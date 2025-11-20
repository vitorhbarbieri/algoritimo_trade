"""
Coletor de dividendos de ações brasileiras
Utiliza múltiplas APIs com fallback automático:
1. Brapi.dev (primária)
2. IbovFinancials (fallback)
3. yfinance (fallback)
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging
import time
import threading
from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Throttle global para evitar rate limits
_last_request_time = {}
_throttle_lock = threading.Lock()

# Tokens das APIs (configurados pelo usuário)
BRAPI_TOKEN = "58XDDJREpzCzHknHU6kTVk"
IBOVFINANCIALS_TOKEN = "719d35865a8af526c715f5bbbca83c1e9579acb4"

def _throttle(api_name: str = 'brapi', min_seconds: float = 1.0):
    """Garante um intervalo mínimo entre requisições."""
    global _last_request_time
    with _throttle_lock:
        now = time.time()
        last = _last_request_time.get(api_name, 0)
        elapsed = now - last
        if elapsed < min_seconds:
            time.sleep(min_seconds - elapsed)
        _last_request_time[api_name] = time.time()

def _criar_sessao_http() -> Session:
    """Cria uma sessão HTTP com retry e headers apropriados."""
    sess = Session()
    retry_strategy = Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    return sess

def _normalizar_ticker_b3(ticker: str) -> str:
    """
    Normaliza o ticker para formato B3.
    Remove .SA se existir para usar na API Brapi.
    """
    if not isinstance(ticker, str) or len(ticker.strip()) == 0:
        return ticker
    tk = ticker.strip().upper()
    # Remove .SA se existir (Brapi usa sem sufixo)
    if tk.endswith('.SA'):
        tk = tk[:-3]
    return tk

def _converter_data_iso(data_iso) -> Optional[str]:
    """Converte data ISO para formato YYYY-MM-DD."""
    if not data_iso:
        return None
    try:
        if isinstance(data_iso, str):
            # Formato: "2025-09-22T00:00:00.000Z" -> "2025-09-22"
            data_str = data_iso.split("T")[0]
            # Validar formato
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        elif isinstance(data_iso, (int, float)):
            dt = datetime.fromtimestamp(data_iso)
            return dt.strftime("%Y-%m-%d")
        else:
            return str(data_iso)[:10]
    except Exception as e:
        logger.warning(f"⚠️  [DIVIDENDOS] Erro ao processar data {data_iso}: {str(e)[:50]}")
        return None

def coletar_dividendos_brapi(ticker: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Coleta dividendos de uma ação usando a API Brapi.dev.
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'BBSE3')
        limit: Número máximo de dividendos a retornar (padrão: 100)
    
    Returns:
        Lista de dicionários com informações de dividendos:
        [
            {
                'data_pagamento': '2025-01-15',
                'ticker': 'PETR4',
                'valor_por_acao': 0.25,
                'tipo': 'DIVIDENDO',
                'data_ex': '2025-01-10',
                'valor_total': 0.0  # Será calculado depois com quantidade
            },
            ...
        ]
    """
    try:
        ticker_norm = _normalizar_ticker_b3(ticker)
        sess = _criar_sessao_http()
        _throttle(1.2)  # Throttle de 1.2 segundos entre requisições
        
        # Verificar se há API key configurada (variável de ambiente ou token padrão)
        api_key = os.getenv("BRAPI_API_KEY") or os.getenv("BRAPI_TOKEN") or BRAPI_TOKEN
        
        # Brapi.dev endpoint para dividendos
        url = f"https://brapi.dev/api/quote/{ticker_norm}?dividends=true"
        if api_key:
            url += f"&token={api_key}"
            logger.debug(f"🔑 [DIVIDENDOS] Usando API key para {ticker}")
        
        logger.info(f"🔍 [DIVIDENDOS] Buscando dividendos para {ticker} via Brapi.dev...")
        
        resp = sess.get(url, timeout=15)
        
        if resp.status_code != 200:
            if resp.status_code == 401:
                logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou 401 (Unauthorized) para {ticker}. Ticker pode não estar disponível na API gratuita.")
            elif resp.status_code == 403:
                try:
                    error_msg = resp.json().get("message", "")
                    if "dividendos" in error_msg.lower() or "dividends" in error_msg.lower():
                        logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou 403 para {ticker}. Seu plano não permite acesso a dividendos. Considere fazer upgrade em brapi.dev/dashboard")
                    else:
                        logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou 403 (Forbidden) para {ticker}")
                except:
                    logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou 403 (Forbidden) para {ticker}")
            elif resp.status_code == 404:
                logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou 404 (Not Found) para {ticker}. Ticker não encontrado.")
            else:
                logger.warning(f"⚠️  [DIVIDENDOS] Brapi.dev retornou status {resp.status_code} para {ticker}")
            return []
        
        try:
            data = resp.json() or {}
        except Exception as e:
            logger.error(f"❌ [DIVIDENDOS] Erro ao parsear JSON para {ticker}: {str(e)[:100]}")
            return []
        
        results = data.get("results") or []
        
        if not results:
            logger.warning(f"⚠️  [DIVIDENDOS] Nenhum resultado encontrado para {ticker}")
            return []
        
        result = results[0]
        
        # Brapi retorna dividendsData com cashDividends, stockDividends, subscriptions
        dividends_data = result.get("dividendsData") or {}
        cash_dividends = dividends_data.get("cashDividends") or []
        stock_dividends = dividends_data.get("stockDividends") or []
        
        # Combinar dividendos em dinheiro e em ações
        all_dividends = cash_dividends + stock_dividends
        
        if not all_dividends:
            logger.info(f"ℹ️  [DIVIDENDOS] Nenhum dividendo encontrado para {ticker}")
            return []
        
        logger.info(f"📊 [DIVIDENDOS] {ticker}: {len(cash_dividends)} dividendos em dinheiro, {len(stock_dividends)} em ações")
        
        # Processar dividendos
        dividendos_processados = []
        for div in all_dividends[:limit]:
            try:
                # Brapi retorna: paymentDate, rate, label, lastDatePrior, etc.
                payment_date = div.get("paymentDate")
                ex_date = div.get("lastDatePrior")  # Data ex-dividendo (data a partir da qual ações são negociadas sem direito)
                label = div.get("label") or ""
                # 'rate' é o valor por ação
                value = float(div.get("rate") or div.get("value") or div.get("amount") or 0)
                
                # Determinar tipo
                tipo = "DIVIDENDO"
                label_upper = label.upper()
                if "JCP" in label_upper or "JSCP" in label_upper:
                    tipo = "JCP"
                elif "RENDIMENTO" in label_upper:
                    tipo = "RENDIMENTO"
                
                # Converter data de pagamento
                data_pagamento = _converter_data_iso(payment_date) or datetime.now().strftime("%Y-%m-%d")
                
                # Converter data ex-dividendo (CRÍTICO: é esta data que determina se recebeu o dividendo)
                data_ex_dividendo = _converter_data_iso(ex_date)
                
                # Se não tiver data ex-dividendo, usar data de pagamento como fallback (não ideal, mas melhor que nada)
                if not data_ex_dividendo:
                    logger.warning(f"⚠️  [DIVIDENDOS] {ticker}: Dividendo {data_pagamento} sem data ex-dividendo. Usando data de pagamento como fallback.")
                    data_ex_dividendo = data_pagamento
                
                dividendos_processados.append({
                    'data_pagamento': data_pagamento,
                    'data_ex_dividendo': data_ex_dividendo,  # Data ex-dividendo (usada para verificar elegibilidade)
                    'ticker': ticker_norm,
                    'valor_por_acao': value,
                    'tipo': tipo,
                    'label': label,
                    'valor_total': 0.0  # Será calculado depois com a quantidade de ações
                })
            except Exception as e:
                logger.warning(f"⚠️  [DIVIDENDOS] Erro ao processar dividendo: {str(e)[:100]}")
                continue
        
        logger.info(f"✅ [DIVIDENDOS] {len(dividendos_processados)} dividendos encontrados para {ticker}")
        return dividendos_processados
        
    except Exception as e:
        logger.error(f"❌ [DIVIDENDOS] Erro ao buscar dividendos para {ticker}: {str(e)[:150]}")
        return []

def coletar_dividendos_yfinance(ticker: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Coleta dividendos usando yfinance (Yahoo Finance).
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'BBSE3')
        limit: Número máximo de dividendos a retornar
    
    Returns:
        Lista de dicionários com informações de dividendos no formato padrão
    """
    try:
        import yfinance as yf
        
        ticker_norm = _normalizar_ticker_b3(ticker)
        _throttle('yfinance', 0.5)  # Throttle menor para yfinance
        
        logger.info(f"🔍 [DIVIDENDOS] Buscando dividendos para {ticker} via yfinance...")
        
        # yfinance requer .SA para ações brasileiras
        ticker_yf = f"{ticker_norm}.SA"
        ticker_obj = yf.Ticker(ticker_yf)
        
        # Buscar dividendos - usar download com período maior para garantir dados
        try:
            # Tentar buscar histórico completo
            dividends = ticker_obj.dividends
        except Exception as e:
            logger.warning(f"⚠️  [DIVIDENDOS] yfinance: Erro ao buscar dividendos para {ticker_yf}: {str(e)[:100]}")
            return []
        
        # Verificar se realmente tem dados válidos
        if dividends is None or len(dividends) == 0:
            logger.info(f"ℹ️  [DIVIDENDOS] yfinance: Nenhum dividendo encontrado para {ticker} (ticker: {ticker_yf})")
            return []
        
        # Verificar se há dados válidos (não apenas NaN ou zeros)
        dividends_validos = dividends.dropna()
        if len(dividends_validos) == 0:
            logger.info(f"ℹ️  [DIVIDENDOS] yfinance: Apenas valores inválidos encontrados para {ticker}")
            return []
        
        logger.info(f"📊 [DIVIDENDOS] yfinance: {len(dividends_validos)} dividendos válidos encontrados para {ticker}")
        
        # Converter para formato padrão
        dividendos_processados = []
        for data, valor in dividends_validos.items():
            if len(dividendos_processados) >= limit:
                break
                
            try:
                # yfinance retorna pandas Timestamp
                if hasattr(data, 'strftime'):
                    data_pagamento = data.strftime('%Y-%m-%d')
                else:
                    data_pagamento = str(data)[:10]
                
                # yfinance não fornece data ex-dividendo diretamente
                # Vamos estimar como 1 dia útil antes da data de pagamento (aproximação)
                # NOTA: Isso não é ideal, mas é melhor que nada
                try:
                    data_pag_dt = datetime.strptime(data_pagamento, '%Y-%m-%d')
                    # Subtrair 1 dia útil (aproximação)
                    data_ex_dividendo = (data_pag_dt - timedelta(days=1)).strftime('%Y-%m-%d')
                except:
                    data_ex_dividendo = data_pagamento
                
                # Determinar tipo (yfinance não fornece, então assumimos DIVIDENDO)
                tipo = "DIVIDENDO"
                
                dividendos_processados.append({
                    'data_pagamento': data_pagamento,
                    'data_ex_dividendo': data_ex_dividendo,  # Estimada
                    'ticker': ticker_norm,
                    'valor_por_acao': float(valor),
                    'tipo': tipo,
                    'label': 'Dividendo',
                    'valor_total': 0.0
                })
            except Exception as e:
                logger.warning(f"⚠️  [DIVIDENDOS] yfinance: Erro ao processar dividendo: {str(e)[:100]}")
                continue
        
        logger.info(f"✅ [DIVIDENDOS] yfinance: {len(dividendos_processados)} dividendos processados para {ticker}")
        return dividendos_processados
        
    except ImportError:
        logger.error("❌ [DIVIDENDOS] yfinance não está instalado. Execute: pip install yfinance")
        return []
    except Exception as e:
        logger.error(f"❌ [DIVIDENDOS] yfinance: Erro ao buscar dividendos para {ticker}: {str(e)[:150]}")
        return []

def coletar_dividendos_ibovfinancials(ticker: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Coleta dividendos usando a API IbovFinancials.
    
    NOTA: Esta API está temporariamente desabilitada devido a problemas com endpoints.
    Os endpoints testados retornaram erro 400 e problemas de DNS.
    Para reativar, é necessário verificar a documentação oficial da API.
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'BBSE3')
        limit: Número máximo de dividendos a retornar
    
    Returns:
        Lista vazia (API desabilitada temporariamente)
    """
    # API temporariamente desabilitada - endpoints não estão funcionando
    # Os endpoints testados retornaram erro 400 e problemas de DNS
    # Para reativar, é necessário verificar a documentação oficial da API IbovFinancials
    logger.warning(f"⚠️  [DIVIDENDOS] IbovFinancials está temporariamente desabilitada para {ticker} (endpoints não funcionam)")
    return []

def coletar_dividendos(ticker: str, limit: int = 100, fontes_preferidas: Optional[List[str]] = None) -> Tuple[List[Dict[str, Any]], str]:
    """
    Coleta dividendos tentando múltiplas APIs em ordem de prioridade (com fallback automático).
    
    Ordem de tentativa:
    1. Brapi.dev (primária) - ✅ Funcionando
    2. yfinance (fallback) - ⚠️ Pode ter limitações
    3. IbovFinancials (desabilitada temporariamente) - ❌ Endpoints não funcionam
    
    Args:
        ticker: Código da ação (ex: 'PETR4', 'BBSE3')
        limit: Número máximo de dividendos a retornar
        fontes_preferidas: Lista de fontes para tentar (ex: ['brapi', 'yfinance']). 
                          Se None, usa ordem padrão.
    
    Returns:
        Tupla (lista_de_dividendos, fonte_usada)
    """
    if fontes_preferidas is None:
        # Removido 'ibovfinancials' da lista padrão até que endpoints sejam corrigidos
        fontes_preferidas = ['brapi', 'yfinance']
    
    ultimo_erro = None
    
    for fonte in fontes_preferidas:
        try:
            if fonte.lower() == 'brapi':
                dividendos = coletar_dividendos_brapi(ticker, limit)
                if dividendos:
                    logger.info(f"✅ [DIVIDENDOS] {ticker}: Sucesso com Brapi.dev ({len(dividendos)} dividendos)")
                    return dividendos, 'brapi.dev'
                else:
                    logger.info(f"ℹ️  [DIVIDENDOS] {ticker}: Brapi.dev não retornou dividendos, tentando próxima fonte...")
                    
            elif fonte.lower() == 'ibovfinancials':
                dividendos = coletar_dividendos_ibovfinancials(ticker, limit)
                if dividendos:
                    logger.info(f"✅ [DIVIDENDOS] {ticker}: Sucesso com IbovFinancials ({len(dividendos)} dividendos)")
                    return dividendos, 'ibovfinancials'
                else:
                    logger.info(f"ℹ️  [DIVIDENDOS] {ticker}: IbovFinancials não retornou dividendos, tentando próxima fonte...")
                    
            elif fonte.lower() == 'yfinance':
                dividendos = coletar_dividendos_yfinance(ticker, limit)
                if dividendos:
                    logger.info(f"✅ [DIVIDENDOS] {ticker}: Sucesso com yfinance ({len(dividendos)} dividendos)")
                    return dividendos, 'yfinance'
                else:
                    logger.info(f"ℹ️  [DIVIDENDOS] {ticker}: yfinance não retornou dividendos")
                    
        except Exception as e:
            ultimo_erro = e
            logger.warning(f"⚠️  [DIVIDENDOS] {ticker}: Erro com {fonte}: {str(e)[:100]}")
            continue
    
    # Se chegou aqui, nenhuma fonte funcionou
    logger.error(f"❌ [DIVIDENDOS] {ticker}: Todas as fontes falharam. Último erro: {str(ultimo_erro)[:150] if ultimo_erro else 'N/A'}")
    return [], 'nenhuma'

def coletar_dividendos_multiplos_tickers(tickers: List[str], limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
    """
    Coleta dividendos para múltiplos tickers usando fallback automático.
    
    Args:
        tickers: Lista de códigos de ações
        limit: Número máximo de dividendos por ticker
    
    Returns:
        Dicionário com ticker como chave e lista de dividendos como valor
    """
    resultado = {}
    for ticker in tickers:
        try:
            dividendos, fonte = coletar_dividendos(ticker, limit)
            resultado[ticker] = dividendos
            logger.debug(f"📊 [DIVIDENDOS] {ticker}: {len(dividendos)} dividendos obtidos via {fonte}")
        except Exception as e:
            logger.warning(f"⚠️  [DIVIDENDOS] Erro ao buscar dividendos para {ticker}: {str(e)[:100]}")
            resultado[ticker] = []
    return resultado

def sincronizar_dividendos_automatico(tickers: List[str] = None, forcar_atualizacao: bool = False) -> Dict[str, Any]:
    """
    Sincroniza dividendos automaticamente da API Brapi.dev.
    Usa cache inteligente: só busca se dados não existem ou são antigos (> 24h).
    
    Args:
        tickers: Lista de tickers. Se None, usa posições abertas da carteira.
        forcar_atualizacao: Se True, força busca mesmo se dados são recentes.
    
    Returns:
        Dicionário com estatísticas da sincronização
    """
    from data.trades_repository import positions_summary, insert_dividendos_rows, verificar_necessidade_sincronizacao_dividendos
    
    # Buscar posições abertas se tickers não fornecidos
    if not tickers:
        logger.info("ℹ️  [DIVIDENDOS] Nenhum ticker fornecido. Buscando posições abertas...")
        resumo = positions_summary()
        posicoes = resumo.get('positions', [])
        if not posicoes:
            logger.warning("⚠️  [DIVIDENDOS] Nenhuma posição aberta encontrada. Não é possível sincronizar dividendos sem posições.")
            return {"status": "erro", "mensagem": "Nenhuma posição aberta encontrada. Importe operações primeiro."}
        tickers = [p['ticker'] for p in posicoes]
        logger.info(f"✅ [DIVIDENDOS] Encontradas {len(tickers)} posições abertas: {tickers}")
    
    logger.info(f"🔄 [DIVIDENDOS] Iniciando sincronização automática para {len(tickers)} tickers: {tickers}")
    
    total_encontrados = 0
    total_importados = 0
    total_em_cache = 0
    erros = []
    
    # Buscar dividendos para cada ticker
    for ticker in tickers:
        try:
            # Verificar se precisa sincronizar
            if not forcar_atualizacao and not verificar_necessidade_sincronizacao_dividendos(ticker):
                logger.info(f"ℹ️  [DIVIDENDOS] {ticker}: Dados em cache são recentes, pulando...")
                total_em_cache += 1
                continue
            
            logger.info(f"🔍 [DIVIDENDOS] Buscando dividendos para {ticker}...")
            fonte_usada = "brapi.dev"  # Default
            try:
                dividendos, fonte_usada = coletar_dividendos(ticker, limit=200)
                logger.info(f"📊 [DIVIDENDOS] {ticker}: Dados obtidos via {fonte_usada}")
            except Exception as e_busca:
                logger.error(f"❌ [DIVIDENDOS] Erro ao buscar dividendos para {ticker}: {str(e_busca)[:150]}")
                erros.append(f"{ticker}: Erro na busca - {str(e_busca)[:100]}")
                continue
            
            if not dividendos:
                logger.info(f"ℹ️  [DIVIDENDOS] {ticker}: Nenhum dividendo encontrado na API")
                continue
            
            total_encontrados += len(dividendos)
            
            # Buscar primeira data de compra do ticker
            from data.trades_repository import calcular_quantidade_acoes_na_data
            resumo = positions_summary()
            posicoes = resumo.get('positions', [])
            posicao = next((p for p in posicoes if p['ticker'] == ticker), None)
            
            primeira_compra = posicao.get('first_buy_date') if posicao else None
            
            if not primeira_compra:
                logger.warning(f"⚠️  [DIVIDENDOS] {ticker}: Não foi possível determinar primeira compra. Verificando operações...")
                # Buscar primeira compra diretamente do banco
                from data.trades_repository import init_db
                import sqlite3
                init_db()
                db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trades.db")
                conn = sqlite3.connect(db_path)
                try:
                    cur = conn.execute(
                        "SELECT MIN(trade_date) FROM trades WHERE ticker = ? AND side = 'BUY'",
                        (ticker,)
                    )
                    row = cur.fetchone()
                    primeira_compra = row[0] if row and row[0] else None
                finally:
                    conn.close()
            
            if not primeira_compra:
                logger.warning(f"⚠️  [DIVIDENDOS] {ticker}: Nenhuma compra encontrada. Dividendos não serão importados.")
                continue
            
            logger.info(f"📅 [DIVIDENDOS] {ticker}: Primeira compra em {primeira_compra}")
            
            # Preparar dados para importação - apenas dividendos recebidos
            # REGRA: Para receber um dividendo, você precisa ter a ação ANTES da data ex-dividendo
            # Se comprou ANTES da data ex-dividendo → RECEBE
            # Se comprou NA ou DEPOIS da data ex-dividendo → NÃO recebe
            rows_to_import = []
            dividendos_recebidos = 0
            dividendos_ignorados = 0
            
            for div in dividendos:
                data_pagamento = div['data_pagamento']
                data_ex_dividendo = div.get('data_ex_dividendo') or data_pagamento
                
                # REGRA CORRETA: Verificar se comprou ANTES da data ex-dividendo
                # Se primeira_compra >= data_ex_dividendo, NÃO recebeu (comprou na ou depois da data ex)
                if primeira_compra >= data_ex_dividendo:
                    dividendos_ignorados += 1
                    logger.debug(f"  ⏭️  Dividendo {data_pagamento} (ex: {data_ex_dividendo}) ignorado - compra ({primeira_compra}) foi na ou depois da data ex-dividendo")
                    continue
                
                # Calcular quantidade de ações na DATA EX-DIVIDENDO (não na data de pagamento!)
                # É preciso ter ações ANTES da data ex-dividendo para receber
                quantidade_acoes = calcular_quantidade_acoes_na_data(ticker, data_ex_dividendo)
                
                if quantidade_acoes <= 0:
                    dividendos_ignorados += 1
                    logger.debug(f"  ⏭️  Dividendo {data_pagamento} (ex: {data_ex_dividendo}) ignorado - sem ações na data ex-dividendo")
                    continue
                
                # Calcular valor total recebido
                valor_total = div['valor_por_acao'] * quantidade_acoes
                dividendos_recebidos += 1
                
                rows_to_import.append({
                    'data_pagamento': data_pagamento,
                    'data_ex_dividendo': data_ex_dividendo,  # Salvar data ex-dividendo
                    'ticker': ticker,
                    'valor_por_acao': div['valor_por_acao'],
                    'quantidade_acoes': quantidade_acoes,
                    'tipo': div['tipo'],
                    'valor_total': valor_total
                })
            
            logger.info(f"📊 [DIVIDENDOS] {ticker}: {dividendos_recebidos} recebidos, {dividendos_ignorados} ignorados (compra após data ex-dividendo ou sem ações)")
            
            # Importar no banco (com INSERT OR IGNORE para evitar duplicatas)
            if rows_to_import:
                resultado = insert_dividendos_rows(rows_to_import, fonte=fonte_usada)
                importados = resultado.get('inserted', 0)
                skipped = resultado.get('skipped', 0)
                total_importados += importados
                logger.info(f"✅ [DIVIDENDOS] {ticker}: {importados} novos dividendos importados ({skipped} já existiam) via {fonte_usada}")
        
        except Exception as e:
            erro_msg = f"Erro ao processar {ticker}: {str(e)[:100]}"
            erros.append(erro_msg)
            logger.error(f"❌ [DIVIDENDOS] {erro_msg}")
    
    logger.info(f"✅ [DIVIDENDOS] Sincronização concluída:")
    logger.info(f"   - Tickers processados: {len(tickers)}")
    logger.info(f"   - Dividendos encontrados: {total_encontrados}")
    logger.info(f"   - Novos dividendos importados: {total_importados}")
    logger.info(f"   - Tickers em cache (dados recentes): {total_em_cache}")
    if erros:
        logger.warning(f"   - Erros: {len(erros)}")
    
    return {
        "status": "ok",
        "total_encontrados": total_encontrados,
        "total_importados": total_importados,
        "total_em_cache": total_em_cache,
        "tickers_processados": len(tickers),
        "erros": erros
    }

def importar_dividendos_automatico(tickers: List[str], data_inicio: Optional[str] = None) -> Dict[str, Any]:
    """
    Busca dividendos automaticamente e importa para o banco de dados.
    
    Args:
        tickers: Lista de tickers para buscar dividendos
        data_inicio: Data de início para filtrar (formato: 'YYYY-MM-DD'). Se None, busca todos.
    
    Returns:
        Dicionário com estatísticas da importação
    """
    from data.trades_repository import positions_summary, insert_dividendos_rows
    
    # Buscar posições abertas se tickers não fornecidos
    if not tickers:
        resumo = positions_summary()
        posicoes = resumo.get('positions', [])
        tickers = [p['ticker'] for p in posicoes]
    
    if not tickers:
        logger.warning("⚠️  [DIVIDENDOS] Nenhum ticker fornecido para buscar dividendos")
        return {"status": "erro", "mensagem": "Nenhum ticker fornecido"}
    
    logger.info(f"🔄 [DIVIDENDOS] Iniciando busca automática de dividendos para {len(tickers)} tickers...")
    
    total_encontrados = 0
    total_importados = 0
    erros = []
    
    # Buscar dividendos para cada ticker
    for ticker in tickers:
        try:
            dividendos, fonte_usada = coletar_dividendos(ticker, limit=200)
            
            if not dividendos:
                continue
            
            # Filtrar por data se fornecida
            if data_inicio:
                dividendos = [d for d in dividendos if d['data_pagamento'] >= data_inicio]
            
            if not dividendos:
                continue
            
            # Buscar quantidade de ações na data do dividendo
            # Por enquanto, vamos usar a quantidade atual da posição
            # TODO: Melhorar para usar quantidade histórica baseada na data do dividendo
            resumo = positions_summary()
            posicoes = resumo.get('positions', [])
            posicao = next((p for p in posicoes if p['ticker'] == ticker), None)
            
            quantidade_acoes = posicao['net_quantity'] if posicao else 0
            
            if quantidade_acoes <= 0:
                logger.warning(f"⚠️  [DIVIDENDOS] {ticker}: Posição zerada ou não encontrada. Dividendos não serão importados (quantidade necessária para calcular valor total).")
                continue
            
            # Preparar dados para importação
            rows_to_import = []
            for div in dividendos:
                # Calcular valor total
                valor_total = div['valor_por_acao'] * quantidade_acoes
                
                rows_to_import.append({
                    'data_pagamento': div['data_pagamento'],
                    'ticker': ticker,
                    'valor_por_acao': div['valor_por_acao'],
                    'quantidade_acoes': quantidade_acoes,
                    'tipo': div['tipo'],
                    'valor_total': valor_total
                })
            
            # Importar no banco
            if rows_to_import:
                resultado = insert_dividendos_rows(rows_to_import)
                importados = resultado.get('inserted', 0)
                total_encontrados += len(dividendos)
                total_importados += importados
                logger.info(f"✅ [DIVIDENDOS] {importados} dividendos importados para {ticker}")
        
        except Exception as e:
            erro_msg = f"Erro ao processar {ticker}: {str(e)[:100]}"
            erros.append(erro_msg)
            logger.error(f"❌ [DIVIDENDOS] {erro_msg}")
    
    return {
        "status": "ok",
        "total_encontrados": total_encontrados,
        "total_importados": total_importados,
        "tickers_processados": len(tickers),
        "erros": erros
    }

