"""
Coletor de dados de preços (OHLCV)
Suporta múltiplos timeframes via yfinance ou API genérica
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging
import time
import math
from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import threading

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _normalizar_ticker_b3(ticker: str) -> str:
    """
    Garante que o ticker tenha o sufixo '.SA' (B3) quando apropriado.
    Não altera quando já há um sufixo (contém '.').
    """
    if not isinstance(ticker, str) or len(ticker.strip()) == 0:
        return ticker
    tk = ticker.strip().upper()
    # Se já tem sufixo como '.SA' ou outro '.', não forçar
    if '.' in tk:
        return tk
    # Para tickers B3 típicos (terminam com dígito/letra da classe), anexar .SA
    return f"{tk}.SA"

def _criar_sessao_http() -> Session:
    """
    Cria sessão HTTP com headers e política de retry para yfinance.
    """
    sess = Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    })
    retry = Retry(
        total=2,
        read=2,
        connect=2,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)
    return sess

_THROTTLE_LOCK = threading.Lock()
_LAST_CALL_TS = 0.0
_CACHE = {}

def _throttle(min_seconds: float = 2.0):
    """
    Espaça chamadas externas para reduzir 429.
    """
    global _LAST_CALL_TS
    with _THROTTLE_LOCK:
        now = time.time()
        delta = now - _LAST_CALL_TS
        if delta < min_seconds:
            time.sleep(min_seconds - delta)
        _LAST_CALL_TS = time.time()

def _ajustar_datas_dias_uteis(inicio: Optional[str], fim: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Ajusta strings de data (YYYY-MM-DD) para o dia útil mais próximo atrás se cair em fds/feriado.
    Usa heurística simples: se DataFrame vier vazio, tentaremos -3 dias úteis depois no fluxo.
    Aqui apenas normalizamos para evitar fim < inicio e remover futura.
    """
    if not inicio and not fim:
        return inicio, fim
    hoje = datetime.now().date()
    inicio_dt = datetime.strptime(inicio, "%Y-%m-%d").date() if inicio else None
    fim_dt = datetime.strptime(fim, "%Y-%m-%d").date() if fim else None
    if fim_dt and fim_dt > hoje:
        fim_dt = hoje
    if inicio_dt and fim_dt and fim_dt < inicio_dt:
        inicio_dt, fim_dt = fim_dt, inicio_dt
    inicio_s = inicio_dt.strftime("%Y-%m-%d") if inicio_dt else None
    fim_s = fim_dt.strftime("%Y-%m-%d") if fim_dt else None
    return inicio_s, fim_s

def _validar_e_corrigir_intervalo_periodo(periodo: Optional[str], intervalo: str, inicio: Optional[str], fim: Optional[str]) -> tuple[str, Optional[str], Optional[str]]:
    """
    Garante combinações válidas de interval/period/start/end segundo regras do Yahoo:
    - 1m: period <= 7d e sem start/end (ou start/end recentes)
    - 2m/5m/15m/30m/60m/90m/1h: period <= 60d
    - 1d/5d/1wk/1mo/3mo: sem restrição rígida
    Se start/end forem passados para intraday com janela maior, convertemos para um period compatível.
    """
    intervalo = intervalo.strip()
    intraday = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]
    if intervalo in intraday:
        # Se recebeu start/end, converte para period com limite de 60d (1m exige 7d)
        if inicio or fim:
            if intervalo == "1m":
                periodo_ajustado = "7d"
            else:
                periodo_ajustado = "60d"
            logger.info(f"ℹ️  [PRICE_COLLECTOR] Intervalo intraday com start/end detectado. Convertendo para period='{periodo_ajustado}'.")
            return intervalo, periodo_ajustado, None
        # Se não veio period, definir padrão compatível
        if not periodo:
            periodo = "60d" if intervalo != "1m" else "7d"
    else:
        # Diários ou superiores: aceitar start/end ou period
        if not periodo and not (inicio and fim):
            periodo = "6mo"
    return intervalo, periodo, fim

def _tentar_download(ticker: str, periodo: str, intervalo: str, inicio: Optional[str], fim: Optional[str]) -> pd.DataFrame:
    """Tenta usar yf.download()"""
    if inicio and fim:
        logger.info(f"📋 [PRICE_COLLECTOR] Chamando yf.download() com parâmetros:")
        logger.info(f"   ticker (posicional) = '{ticker}'")
        logger.info(f"   start = '{inicio}'")
        logger.info(f"   end = '{fim}'")
        logger.info(f"   interval = '{intervalo}'")
        logger.info(f"   progress = False")
        logger.info(f"   timeout = 20")
        logger.info(f"   Comando completo: yf.download('{ticker}', start='{inicio}', end='{fim}', interval='{intervalo}', progress=False, timeout=20)")
        print(f"[SIM] Executando: yf.download('{ticker}', start='{inicio}', end='{fim}', interval='{intervalo}', progress=False, timeout=20)")
        sess = _criar_sessao_http()
        return yf.download(ticker, start=inicio, end=fim, interval=intervalo, progress=False, timeout=20, auto_adjust=True, actions=False, repair=True, session=sess, threads=False)
    else:
        logger.info(f"📋 [PRICE_COLLECTOR] Chamando yf.download() com parâmetros:")
        logger.info(f"   ticker (posicional) = '{ticker}'")
        logger.info(f"   period = '{periodo}'")
        logger.info(f"   interval = '{intervalo}'")
        logger.info(f"   progress = False")
        logger.info(f"   timeout = 20")
        logger.info(f"   Comando completo: yf.download('{ticker}', period='{periodo}', interval='{intervalo}', progress=False, timeout=20)")
        print(f"[SIM] Executando: yf.download('{ticker}', period='{periodo}', interval='{intervalo}', progress=False, timeout=20)")
        sess = _criar_sessao_http()
        return yf.download(ticker, period=periodo, interval=intervalo, progress=False, timeout=20, auto_adjust=True, actions=False, repair=True, session=sess, threads=False)


def _tentar_ticker_history(ticker: str, periodo: str, intervalo: str, inicio: Optional[str], fim: Optional[str]) -> pd.DataFrame:
    """Tenta usar Ticker.history() - às vezes funciona melhor que download()"""
    logger.info(f"📋 [PRICE_COLLECTOR] Criando objeto yf.Ticker('{ticker}')")
    sess = _criar_sessao_http()
    ticker_obj = yf.Ticker(ticker, session=sess)
    
    if inicio and fim:
        params = {
            'start': inicio,
            'end': fim,
            'interval': intervalo,
            'timeout': 20,
            'auto_adjust': True,
            'actions': False,
            'repair': True
        }
        logger.info(f"📋 [PRICE_COLLECTOR] Chamando ticker_obj.history() com parâmetros:")
        logger.info(f"   start = {params['start']}")
        logger.info(f"   end = {params['end']}")
        logger.info(f"   interval = {params['interval']}")
        logger.info(f"   timeout = {params['timeout']}")
        logger.info(f"   Comando completo: yf.Ticker('{ticker}').history(start='{inicio}', end='{fim}', interval='{intervalo}', timeout=20)")
        print(f"[SIM] Executando: yf.Ticker('{ticker}').history(start='{inicio}', end='{fim}', interval='{intervalo}', timeout=20)")
        return ticker_obj.history(**params)
    else:
        # Converter periodo para timedelta
        periodos = {
            '1d': timedelta(days=1),
            '5d': timedelta(days=5),
            '1mo': timedelta(days=30),
            '3mo': timedelta(days=90),
            '6mo': timedelta(days=180),
            '1y': timedelta(days=365),
            '2y': timedelta(days=730),
            '5y': timedelta(days=1825),
        }
        
        if periodo in periodos:
            fim_date = datetime.now()
            inicio_date = fim_date - periodos[periodo]
            inicio_str = inicio_date.strftime('%Y-%m-%d')
            params = {
                'start': inicio_str,
                'interval': intervalo,
                'timeout': 20,
                'auto_adjust': True,
                'actions': False,
                'repair': True
            }
            logger.info(f"📋 [PRICE_COLLECTOR] Chamando ticker_obj.history() com parâmetros (periodo convertido):")
            logger.info(f"   start = {params['start']} (calculado de periodo='{periodo}')")
            logger.info(f"   interval = {params['interval']}")
            logger.info(f"   timeout = {params['timeout']}")
            logger.info(f"   Comando completo: yf.Ticker('{ticker}').history(start='{inicio_str}', interval='{intervalo}', timeout=20)")
            print(f"[SIM] Executando: yf.Ticker('{ticker}').history(start='{inicio_str}', interval='{intervalo}', timeout=20)")
            return ticker_obj.history(**params)
        else:
            params = {
                'period': periodo,
                'interval': intervalo,
                'timeout': 20,
                'auto_adjust': True,
                'actions': False,
                'repair': True
            }
            logger.info(f"📋 [PRICE_COLLECTOR] Chamando ticker_obj.history() com parâmetros:")
            logger.info(f"   period = {params['period']}")
            logger.info(f"   interval = {params['interval']}")
            logger.info(f"   timeout = {params['timeout']}")
            logger.info(f"   Comando completo: yf.Ticker('{ticker}').history(period='{periodo}', interval='{intervalo}', timeout=20)")
            print(f"[SIM] Executando: yf.Ticker('{ticker}').history(period='{periodo}', interval='{intervalo}', timeout=20)")
            return ticker_obj.history(**params)


def coletar_precos(
    ticker: str,
    periodo: str = "1mo",
    intervalo: str = "1d",
    inicio: Optional[str] = None,
    fim: Optional[str] = None
) -> pd.DataFrame:
    """
    Coleta dados de preços OHLCV
    
    Args:
        ticker: Código da ação (ex: 'ITUB4.SA', 'PETR4.SA')
        periodo: Período para buscar ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        intervalo: Intervalo dos dados ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        inicio: Data inicial (formato 'YYYY-MM-DD') - opcional
        fim: Data final (formato 'YYYY-MM-DD') - opcional
    
    Returns:
        DataFrame com colunas: Open, High, Low, Close, Volume
    """
    logger.info(f"🔍 [PRICE_COLLECTOR] Iniciando coleta de preços para {ticker}")
    logger.info(f"   Parâmetros: periodo={periodo}, intervalo={intervalo}, inicio={inicio}, fim={fim}")
    intervalo = intervalo.strip()
    
    # Normalizar ticker para B3 se aplicável
    ticker_original = ticker
    ticker = _normalizar_ticker_b3(ticker)
    if ticker != ticker_original:
        logger.info(f"ℹ️  [PRICE_COLLECTOR] Normalizando ticker: {ticker_original} -> {ticker}")
    
    # Validar/ajustar intervalo x periodo x datas
    inicio, fim = _ajustar_datas_dias_uteis(inicio, fim)
    intervalo, periodo, fim = _validar_e_corrigir_intervalo_periodo(periodo, intervalo, inicio, fim)
    logger.info(f"ℹ️  [PRICE_COLLECTOR] Parâmetros ajustados: periodo={periodo}, intervalo={intervalo}, inicio={inicio}, fim={fim}")
    
    # Primeiro: tentar via Yahoo Chart v8 para histórico (preferido)
    try:
        df_chart = _coletar_historico_via_yahoo_chart(
            ticker,
            range_="1mo" if (inicio is None and fim is None) else "5d",
            interval=intervalo if (inicio is None and fim is None) else "1d"
        )
        logger.info(f"✅ [PRICE_COLLECTOR] Histórico via Chart obtido: {len(df_chart)} períodos")
        dados = df_chart.copy()
        ticker_funcionou = ticker
    except Exception as e_chart_hist:
        logger.warning(f"⚠️  [PRICE_COLLECTOR] Chart histórico falhou: {str(e_chart_hist)[:150]}")
        # Continua para tentativas via yfinance
        dados = pd.DataFrame()
        ticker_funcionou = None

    if not dados.empty:
        # Pule tentativas yfinance se já temos dados
        pass
    else:
        # Tentar variações do ticker se falhar
        variacoes_ticker = [ticker]
        
        # Se termina com .SA, tentar sem .SA também
        if ticker.endswith('.SA'):
            variacoes_ticker.append(ticker[:-3])
        
        # Tentar variações comuns (ex: CMIG4 -> CMIG3, ou vice-versa)
        if len(ticker) >= 5 and ticker[-1].isdigit():
            base = ticker[:-1]
            if ticker.endswith('.SA'):
                base = ticker[:-4]  # Remove .SA e o número
                for num in ['3', '4']:
                    variacoes_ticker.append(f"{base}{num}.SA")
            else:
                base = ticker[:-1]
                for num in ['3', '4']:
                    variacoes_ticker.append(f"{base}{num}.SA")
        
        # Remover duplicatas mantendo ordem
        variacoes_ticker = list(dict.fromkeys(variacoes_ticker))
        
        dados = pd.DataFrame()
        ticker_funcionou = None
        ultimo_erro = None
        
        for ticker_teste in variacoes_ticker:
            # Estratégia de tentativas com backoff e variação de parâmetros
            tentativas = []
            if inicio and fim:
                tentativas.extend([
                    ("download(start/end)", lambda: _tentar_download(ticker_teste, periodo, intervalo, inicio, fim)),
                    ("ticker.history(start/end)", lambda: _tentar_ticker_history(ticker_teste, periodo, intervalo, inicio, fim)),
                ])
                # Se vazio, tentar reduzir janela (ex: fim-3d)
                try_dates = []
                try:
                    fim_dt = datetime.strptime(fim, "%Y-%m-%d").date()
                    for delta in [1, 2, 3, 5]:
                        novo_inicio = (fim_dt - timedelta(days=delta)).strftime("%Y-%m-%d")
                        try_dates.append(novo_inicio)
                except:
                    try_dates = []
                for novo_inicio in try_dates:
                    tentativas.append((f"ticker.history(narrow:{novo_inicio}->{fim})", lambda ni=novo_inicio: _tentar_ticker_history(ticker_teste, periodo, intervalo, ni, fim)))
            else:
                tentativas.extend([
                    ("download(period)", lambda: _tentar_download(ticker_teste, periodo, intervalo, None, None)),
                    ("ticker.history(period)", lambda: _tentar_ticker_history(ticker_teste, periodo, intervalo, None, None)),
                ])
                # Se intraday e vazio, tentar degradar para 1d
                if intervalo in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
                    tentativas.append(("download(period,1d)", lambda: _tentar_download(ticker_teste, periodo, "1d", None, None)))
                    tentativas.append(("ticker.history(period,1d)", lambda: _tentar_ticker_history(ticker_teste, periodo, "1d", None, None)))
            
            for metodo_nome, metodo_func in tentativas:
                try:
                    logger.info(f"📡 [PRICE_COLLECTOR] Tentando {ticker_teste} (método: {metodo_nome})...")
                    
                    dados = metodo_func()
                    
                    logger.info(f"📊 [PRICE_COLLECTOR] Resposta recebida do yfinance para {ticker_teste}")
                    logger.info(f"   Shape: {dados.shape}")
                    logger.info(f"   Colunas: {list(dados.columns)}")
                    logger.info(f"   Índice: {dados.index[:3].tolist() if len(dados) > 0 else 'VAZIO'}...")
                    
                    if not dados.empty:
                        ticker_funcionou = ticker_teste
                        logger.info(f"✅ [PRICE_COLLECTOR] {ticker_teste} funcionou com método {metodo_nome}!")
                        break
                    else:
                        logger.warning(f"⚠️  [PRICE_COLLECTOR] {ticker_teste} retornou DataFrame vazio (método: {metodo_nome})")
                
                except Exception as e:
                    ultimo_erro = str(e)
                    logger.warning(f"⚠️  [PRICE_COLLECTOR] Erro ao tentar {ticker_teste} (método: {metodo_nome}): {str(e)[:150]}")
                    # Se não for JSONDecodeError, adicionar pequeno delay antes de próxima tentativa
                    if "JSONDecodeError" not in str(type(e).__name__):
                        time.sleep(0.5)
                    continue
            
            # Se conseguiu dados, sair do loop de variações
            if not dados.empty:
                break
            
            # Delay entre variações de ticker
            time.sleep(0.3)
    
    if dados.empty:
        logger.error(f"❌ [PRICE_COLLECTOR] Nenhuma variação do ticker funcionou")
        logger.error(f"   Tentadas: {variacoes_ticker}")
        logger.error(f"   Último erro: {ultimo_erro}")
        raise ValueError(f"Nenhum dado encontrado para {ticker} (tentadas variações: {variacoes_ticker})")
    
    if ticker_funcionou and ticker_funcionou != ticker:
        logger.info(f"ℹ️  [PRICE_COLLECTOR] Ticker corrigido: {ticker} -> {ticker_funcionou}")
    
    logger.info(f"✅ [PRICE_COLLECTOR] Dados recebidos: {len(dados)} períodos (ticker usado: {ticker_funcionou or ticker})")
    
    # Garantir que temos as colunas necessárias
    logger.info(f"🔧 [PRICE_COLLECTOR] Processando estrutura dos dados...")
    
    if len(dados.columns) > 1:
        logger.info(f"   Multi-coluna detectado, processando...")
        # Se multi-index, pegar apenas 'Close'
        if 'Close' in dados.columns.get_level_values(0):
            logger.info(f"   Coluna 'Close' encontrada no multi-index")
            dados = dados['Close'].to_frame()
            dados.columns = ['Close']
        else:
            logger.info(f"   Usando primeira coluna como base")
            dados = dados.iloc[:, 0].to_frame()
            dados.columns = ['Close']
    
    # Renomear colunas se necessário
    dados.columns = [col[0] if isinstance(col, tuple) else col for col in dados.columns]
    logger.info(f"   Colunas após processamento: {list(dados.columns)}")
    
    # Garantir colunas padrão
    colunas_necessarias = ['Open', 'High', 'Low', 'Close', 'Volume']
    logger.info(f"🔧 [PRICE_COLLECTOR] Garantindo colunas necessárias: {colunas_necessarias}")
    
    for col in colunas_necessarias:
        if col not in dados.columns:
            logger.info(f"   Adicionando coluna faltante: {col}")
            if col == 'Volume':
                dados[col] = 0
            else:
                dados[col] = dados['Close'] if 'Close' in dados.columns else dados.iloc[:, 0]
    
    # Ordenar por data
    dados = dados.sort_index()
    logger.info(f"   Dados ordenados por data")
    
    # Remover duplicatas
    duplicatas = dados.index.duplicated(keep='first').sum()
    if duplicatas > 0:
        logger.info(f"   Removendo {duplicatas} duplicatas")
    dados = dados[~dados.index.duplicated(keep='first')]
    
    resultado = dados[colunas_necessarias]
    logger.info(f"✅ [PRICE_COLLECTOR] Coleta concluída para {ticker}")
    logger.info(f"   Resultado final: {len(resultado)} períodos")
    logger.info(f"   Primeiro preço: R$ {resultado['Close'].iloc[0]:.2f}")
    logger.info(f"   Último preço: R$ {resultado['Close'].iloc[-1]:.2f}")
    
    return resultado


def coletar_ultimo_pregao(ticker: str, intervalo: str = "1d") -> pd.DataFrame:
    """
    Busca apenas o último pregão publicado (intervalo diário por padrão).
    Estratégia:
      1) Tentar Ticker.history(period='10d', interval='1d') e pegar a última linha disponível.
      2) Se vazio, tentar yf.download(period='10d', interval='1d').
    Retorna DataFrame com 1 linha (Open, High, Low, Close, Volume) ou lança erro.
    """
    logger.info(f"🔍 [PRICE_COLLECTOR] Coletando apenas o último pregão para {ticker}")
    ticker_norm = _normalizar_ticker_b3(ticker)
    if ticker_norm != ticker:
        logger.info(f"ℹ️  [PRICE_COLLECTOR] Normalizando ticker: {ticker} -> {ticker_norm}")
    # Cache: último pregão
    cache_key = ("ultimo", ticker_norm, intervalo)
    now = time.time()
    if cache_key in _CACHE:
        ts_cache, df_cache = _CACHE[cache_key]
        if now - ts_cache <= 120 and df_cache is not None and not df_cache.empty:
            logger.info(f"🗃️  [PRICE_COLLECTOR] Retornando último pregão de cache para {ticker_norm}")
            return df_cache.copy()
    df = pd.DataFrame()
    # Ordem preferida: Chart v8 -> Quote v7 -> brapi.dev -> yfinance
    try:
        logger.info("ℹ️  [PRICE_COLLECTOR] Usando Yahoo Chart v8 para último pregão.")
        df = _coletar_ultimo_preco_via_yahoo_chart(ticker_norm)
    except Exception as e_chart:
        logger.warning(f"⚠️  [PRICE_COLLECTOR] Chart v8 falhou: {str(e_chart)[:150]}")
        try:
            logger.info("ℹ️  [PRICE_COLLECTOR] Fallback para Quote API (v7).")
            df = _coletar_ultimo_preco_via_quote(ticker_norm)
        except Exception as e_quote:
            logger.warning(f"⚠️  [PRICE_COLLECTOR] Quote v7 falhou: {str(e_quote)[:150]}")
            try:
                logger.info("ℹ️  [PRICE_COLLECTOR] Fallback para brapi.dev.")
                df = _coletar_ultimo_preco_via_brapi(ticker_norm)
            except Exception as e_brapi:
                logger.warning(f"⚠️  [PRICE_COLLECTOR] brapi.dev falhou: {str(e_brapi)[:150]}")
                # Último recurso: yfinance (history/download)
                try:
                    sess = _criar_sessao_http()
                    _throttle(2.0)
                    tk = yf.Ticker(ticker_norm, session=sess)
                    print(f"[SIM] Executando: yf.Ticker('{ticker_norm}').history(period='10d', interval='1d', auto_adjust=True, actions=False, repair=True, timeout=20)")
                    df = tk.history(period="10d", interval="1d", auto_adjust=True, actions=False, repair=True, timeout=20)
                    if df is None or df.empty:
                        _throttle(2.0)
                        print(f"[SIM] Executando: yf.download('{ticker_norm}', period='10d', interval='1d', auto_adjust=True, actions=False, repair=True, timeout=20)")
                        df = yf.download(ticker_norm, period="10d", interval="1d", auto_adjust=True, actions=False, repair=True, progress=False, timeout=20, session=sess, threads=False)
                except Exception as e_yf:
                    logger.warning(f"⚠️  [PRICE_COLLECTOR] yfinance falhou: {str(e_yf)[:150]}")
    if df is None or df.empty:
        raise ValueError(f"Não foi possível obter o último pregão para {ticker_norm}")
    df = df.sort_index()
    ultima = df.tail(1)
    # Garantir colunas padrão
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        if col not in ultima.columns:
            if col == 'Volume':
                ultima[col] = 0
            else:
                base = 'Close' if 'Close' in ultima.columns else ultima.columns[0]
                ultima[col] = ultima[base]
    logger.info(f"✅ [PRICE_COLLECTOR] Último pregão obtido para {ticker_norm}: {ultima.index[-1]}")
    # Cache save
    _CACHE[cache_key] = (now, ultima[['Open', 'High', 'Low', 'Close', 'Volume']].copy())
    return _CACHE[cache_key][1].copy()

def _coletar_ultimo_preco_via_quote(ticker: str) -> pd.DataFrame:
    """
    Fallback leve: usa endpoint de quote do Yahoo para pegar preço atual/último.
    Cria DataFrame de 1 linha compatível (Open/High/Low/Close/Volume).
    """
    ticker_norm = _normalizar_ticker_b3(ticker)
    sess = _criar_sessao_http()
    _throttle(1.2)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote"
    params = {"symbols": ticker_norm}
    print(f"[SIM] Executando: GET {url}?symbols={ticker_norm}")
    resp = sess.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        raise ValueError(f"Quote API retornou status {resp.status_code}")
    data = resp.json()
    result = (data.get("quoteResponse") or {}).get("result") or []
    if not result:
        raise ValueError("Quote API sem resultados para o ticker")
    q = result[0]
    price = q.get("regularMarketPrice")
    high = q.get("regularMarketDayHigh", price)
    low = q.get("regularMarketDayLow", price)
    openp = q.get("regularMarketOpen", price)
    volume = q.get("regularMarketVolume", 0) or 0
    ts = q.get("regularMarketTime") or int(time.time())
    dt = datetime.fromtimestamp(ts)
    idx = pd.DatetimeIndex([dt])
    df = pd.DataFrame({
        "Open": [openp if openp is not None else price],
        "High": [high if high is not None else price],
        "Low": [low if low is not None else price],
        "Close": [price],
        "Volume": [volume]
    }, index=idx)
    return df

def _coletar_ultimo_preco_via_yahoo_chart(ticker: str) -> pd.DataFrame:
    """
    Fallback alternativo: usa o endpoint de chart do Yahoo (v8) com range curto.
    Monta OHLCV do último candle disponível em 1d.
    """
    ticker_norm = _normalizar_ticker_b3(ticker)
    sess = _criar_sessao_http()
    _throttle(1.2)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker_norm}"
    params = {"range": "5d", "interval": "1d", "events": "div,split"}
    print(f"[SIM] Executando: GET {url}?range=5d&interval=1d")
    resp = sess.get(url, params=params, timeout=12)
    if resp.status_code != 200:
        raise ValueError(f"Chart API retornou status {resp.status_code}")
    data = resp.json()
    result = (data.get("chart") or {}).get("result") or []
    if not result:
        raise ValueError("Chart API sem resultados")
    r0 = result[0]
    ts = r0.get("timestamp") or []
    ind = (r0.get("indicators") or {}).get("quote") or []
    if not ts or not ind:
        raise ValueError("Chart API sem séries de preços")
    q = ind[0]
    opens = q.get("open") or []
    highs = q.get("high") or []
    lows = q.get("low") or []
    closes = q.get("close") or []
    volumes = q.get("volume") or []
    idx = len(ts) - 1
    if idx < 0 or idx >= len(closes) or closes[idx] is None:
        raise ValueError("Chart API sem candle válido")
    dt = datetime.fromtimestamp(ts[idx])
    df = pd.DataFrame({
        "Open": [opens[idx] if idx < len(opens) else closes[idx]],
        "High": [highs[idx] if idx < len(highs) else closes[idx]],
        "Low": [lows[idx] if idx < len(lows) else closes[idx]],
        "Close": [closes[idx]],
        "Volume": [volumes[idx] if idx < len(volumes) and volumes[idx] is not None else 0],
    }, index=pd.DatetimeIndex([dt]))
    return df

def _coletar_ultimo_preco_via_brapi(ticker: str) -> pd.DataFrame:
    """
    Fallback público: brapi.dev (sem API key para uso leve).
    Tenta com e sem sufixo .SA.
    """
    sess = _criar_sessao_http()
    _throttle(1.2)
    candidatos = []
    t_norm = _normalizar_ticker_b3(ticker)
    candidatos.append(t_norm)
    if t_norm.endswith(".SA"):
        candidatos.append(t_norm[:-3])  # sem .SA
    for t in candidatos:
        url = f"https://brapi.dev/api/quote/{t}"
        print(f"[SIM] Executando: GET {url}")
        resp = sess.get(url, timeout=10)
        if resp.status_code != 200:
            continue
        data = resp.json() or {}
        results = data.get("results") or []
        if not results:
            continue
        r = results[0]
        price = r.get("regularMarketPrice") or r.get("close") or r.get("price")
        openp = r.get("regularMarketOpen") or r.get("open") or price
        high = r.get("regularMarketDayHigh") or r.get("high") or price
        low = r.get("regularMarketDayLow") or r.get("low") or price
        volume = r.get("regularMarketVolume") or r.get("volume") or 0
        # Data/hora
        ts = r.get("regularMarketTime") or r.get("updatedAt")
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(int(ts))
        else:
            try:
                dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            except:
                dt = datetime.now()
        df = pd.DataFrame({
            "Open": [openp],
            "High": [high],
            "Low": [low],
            "Close": [price],
            "Volume": [volume or 0],
        }, index=pd.DatetimeIndex([dt]))
        return df
    raise ValueError("brapi.dev sem resultados")

def coletar_precos_multiplos(
    tickers: list,
    periodo: str = "1mo",
    intervalo: str = "1d"
) -> dict:
    """
    Coleta preços de múltiplos tickers
    
    Args:
        tickers: Lista de códigos de ações
        periodo: Período para buscar
        intervalo: Intervalo dos dados
    
    Returns:
        Dicionário com {ticker: DataFrame}
    """
    dados = {}
    for ticker in tickers:
        try:
            dados[ticker] = coletar_precos(ticker, periodo, intervalo)
        except Exception as e:
            print(f"Erro ao coletar {ticker}: {e}")
            continue
    
    return dados


if __name__ == "__main__":
    # Teste
    print("Testando coletor de preços...")
    # 1) Teste usando period/interval (sem datas)
    df = coletar_precos("ITUB4.SA", periodo="1mo", intervalo="1d")
    print(f"\nDados coletados (period='1mo'):")
    print(df.head())
    print(f"\nShape: {df.shape}")
    # 2) Teste usando start/end para simular data-base específica
    inicio_teste = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    fim_teste = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"\nSimulando com datas: inicio={inicio_teste} fim={fim_teste}")
    df2 = coletar_precos("ITUB4.SA", intervalo="1d", inicio=inicio_teste, fim=fim_teste)
    print(f"\nDados coletados (start/end):")
    print(df2.head())
    print(f"\nShape: {df2.shape}")

