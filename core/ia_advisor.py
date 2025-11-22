"""
Módulo de análise de IA para recomendar movimentos estratégicos na carteira.
Suporta múltiplos provedores de IA (OpenAI, Claude, etc.)
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def analisar_carteira_com_ia(
    positions: List[Dict[str, Any]],
    pnl_carteira: float,
    pnl_realizado: float,
    pnl_total: float,
    rentabilidade_carteira: float,
    rentabilidade_realizada: float,
    rentabilidade_total: float,
    total_investido: float,
    total_valor: float,
    custo_vendas: float,
    receita_vendas: float
) -> Dict[str, Any]:
    """
    Analisa a carteira usando IA e retorna recomendações estratégicas.
    
    Args:
        positions: Lista de posições com ticker, quantidade, preço médio, preço último, rentabilidade
        pnl_carteira: PnL não realizado (posições abertas)
        pnl_realizado: PnL realizado (vendas)
        pnl_total: PnL total
        rentabilidade_carteira: Rentabilidade das posições abertas
        rentabilidade_realizada: Rentabilidade das vendas
        rentabilidade_total: Rentabilidade total
        total_investido: Total investido em posições abertas
        total_valor: Valor atual das posições abertas
        custo_vendas: Custo das ações vendidas
        receita_vendas: Receita das vendas
    
    Returns:
        Dict com recomendações estruturadas da IA
    """
    try:
        # Formatar dados da carteira para o prompt
        carteira_texto = _formatar_carteira_para_prompt(
            positions, pnl_carteira, pnl_realizado, pnl_total,
            rentabilidade_carteira, rentabilidade_realizada, rentabilidade_total,
            total_investido, total_valor, custo_vendas, receita_vendas
        )
        
        # Gerar prompt estruturado
        prompt = _criar_prompt_analise(carteira_texto)
        
        # Chamar IA (tentar OpenAI primeiro, depois fallback)
        recomendacoes = _chamar_ia(prompt)
        
        return {
            "status": "ok",
            "recomendacoes": recomendacoes,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Erro ao analisar carteira com IA: {str(e)}")
        return {
            "status": "erro",
            "erro": str(e),
            "mensagem": "Nenhuma API de IA disponível. Configure OPENAI_API_KEY ou ANTHROPIC_API_KEY para usar análises de IA.",
            "timestamp": datetime.now().isoformat()
        }

def _formatar_carteira_para_prompt(
    positions: List[Dict[str, Any]],
    pnl_carteira: float,
    pnl_realizado: float,
    pnl_total: float,
    rentabilidade_carteira: float,
    rentabilidade_realizada: float,
    rentabilidade_total: float,
    total_investido: float,
    total_valor: float,
    custo_vendas: float,
    receita_vendas: float
) -> str:
    """Formata os dados da carteira em texto estruturado para o prompt."""
    texto = f"""CARTEIRA DE INVESTIMENTOS - ANÁLISE ESTRATÉGICA

RESUMO GERAL:
- Total Investido (Posições Abertas): R$ {total_investido:,.2f}
- Valor Atual (Posições Abertas): R$ {total_valor:,.2f}
- PnL Carteira (Não Realizado): R$ {pnl_carteira:,.2f} ({rentabilidade_carteira*100:.2f}%)
- PnL Realizado (Vendas): R$ {pnl_realizado:,.2f} ({rentabilidade_realizada*100:.2f}%)
- PnL Total: R$ {pnl_total:,.2f} ({rentabilidade_total*100:.2f}%)
- Custo das Vendas: R$ {custo_vendas:,.2f}
- Receita das Vendas: R$ {receita_vendas:,.2f}

POSIÇÕES ABERTAS:
"""
    for pos in positions:
        ticker = pos.get('ticker', 'N/A')
        qty = pos.get('quantidade', 0)
        preco_medio = pos.get('preco_medio', 0)
        preco_ultimo = pos.get('preco_ultimo')
        valor_posicao = pos.get('valor_posicao')
        rentabilidade = pos.get('rentabilidade')
        rentabilidade_anualizada = pos.get('rentabilidade_anualizada')
        
        texto += f"\n- {ticker}:\n"
        texto += f"  Quantidade: {qty}\n"
        texto += f"  Preço Médio: R$ {preco_medio:.2f}\n"
        if preco_ultimo:
            texto += f"  Preço Atual: R$ {preco_ultimo:.2f}\n"
            if valor_posicao:
                texto += f"  Valor da Posição: R$ {valor_posicao:,.2f}\n"
            if rentabilidade is not None:
                texto += f"  Rentabilidade: {rentabilidade*100:.2f}%\n"
            if rentabilidade_anualizada is not None:
                texto += f"  Rentabilidade Anualizada: {rentabilidade_anualizada*100:.2f}%\n"
        else:
            texto += f"  Preço Atual: Não disponível\n"
    
    return texto

def _criar_prompt_analise(carteira_texto: str) -> str:
    """Cria o prompt completo para análise da IA."""
    return f"""Você é um analista especializado em trading e gestão de carteiras de ações brasileiras (B3).

Analise a seguinte carteira e forneça recomendações estratégicas detalhadas:

{carteira_texto}

INSTRUÇÕES:
1. Analise o desempenho de cada posição
2. Identifique oportunidades de otimização
3. Sugira movimentos estratégicos (manter, aumentar, reduzir, vender)
4. Considere diversificação, concentração de risco e rentabilidade
5. Priorize ações com melhor perspectiva de valorização
6. Alerte sobre posições com risco elevado ou baixa rentabilidade

FORMATO DE RESPOSTA (JSON):
{{
  "resumo": "Resumo executivo da análise em 2-3 frases",
  "recomendacoes": [
    {{
      "ticker": "BBSE3",
      "acao": "MANTER|AUMENTAR|REDUZIR|VENDER",
      "justificativa": "Explicação detalhada da recomendação",
      "prioridade": "ALTA|MEDIA|BAIXA",
      "rentabilidade_atual": "X%",
      "perspectiva": "Boa perspectiva de valorização baseada em..."
    }}
  ],
  "observacoes_gerais": [
    "Observação 1 sobre a carteira",
    "Observação 2 sobre diversificação",
    "Observação 3 sobre risco"
  ],
  "sugestoes_estrategicas": [
    "Sugestão estratégica 1",
    "Sugestão estratégica 2"
  ]
}}

Responda APENAS com o JSON válido, sem texto adicional antes ou depois.
"""

def _chamar_ia(prompt: str) -> Dict[str, Any]:
    """Chama a API de IA (OpenAI, Claude, Gemini, Ollama, etc.)"""
    erros = []
    erros_detalhados = []
    
    # Ordem de tentativa: Gratuitas primeiro, depois pagas
    
    # 1. Tentar Google Gemini (GRATUITO)
    try:
        return _chamar_gemini(prompt)
    except Exception as e_gemini:
        erro_msg = str(e_gemini)
        if "não configurada" not in erro_msg.lower() and "not configured" not in erro_msg.lower():
            erros.append("Gemini")
            erros_detalhados.append(f"Gemini: {erro_msg}")
            logger.warning(f"⚠️  Gemini falhou: {erro_msg[:150]}")
    
    # 2. Tentar Ollama (GRATUITO - Local)
    try:
        return _chamar_ollama(prompt)
    except Exception as e_ollama:
        erro_msg = str(e_ollama)
        if "não disponível" not in erro_msg.lower() and "not available" not in erro_msg.lower():
            erros.append("Ollama")
            erros_detalhados.append(f"Ollama: {erro_msg}")
            logger.warning(f"⚠️  Ollama falhou: {erro_msg[:150]}")
    
    # 3. Tentar Groq (GRATUITO)
    try:
        return _chamar_groq(prompt)
    except Exception as e_groq:
        erro_msg = str(e_groq)
        if "não configurada" not in erro_msg.lower() and "not configured" not in erro_msg.lower():
            erros.append("Groq")
            erros_detalhados.append(f"Groq: {erro_msg}")
            logger.warning(f"⚠️  Groq falhou: {erro_msg[:150]}")
    
    # 4. Tentar OpenAI (PAGO)
    try:
        return _chamar_openai(prompt)
    except Exception as e_openai:
        erro_msg = str(e_openai)
        erros.append("OpenAI")
        erros_detalhados.append(f"OpenAI: {erro_msg}")
        logger.warning(f"⚠️  OpenAI falhou: {erro_msg[:150]}")
    
    # 5. Tentar Claude (PAGO)
    try:
        return _chamar_claude(prompt)
    except Exception as e_claude:
        erro_msg = str(e_claude)
        erros.append("Claude")
        erros_detalhados.append(f"Claude: {erro_msg}")
        logger.warning(f"⚠️  Claude falhou: {erro_msg[:150]}")
    
    # Se todas falharam, criar mensagem de erro amigável
    mensagem_erro = "❌ Nenhuma API de IA disponível no momento.\n\n"
    mensagem_erro += "OPÇÕES GRATUITAS RECOMENDADAS:\n\n"
    mensagem_erro += "1. Google Gemini (GRATUITO - Melhor opção):\n"
    mensagem_erro += "   - Obtenha API key em: https://makersuite.google.com/app/apikey\n"
    mensagem_erro += "   - Instale: pip install google-generativeai\n"
    mensagem_erro += "   - Configure: setx GOOGLE_API_KEY sua_chave_aqui\n\n"
    mensagem_erro += "2. Ollama (100% GRATUITO - Local):\n"
    mensagem_erro += "   - Instale: https://ollama.ai/download\n"
    mensagem_erro += "   - Baixe modelo: ollama pull llama2\n"
    mensagem_erro += "   - Instale: pip install ollama\n"
    mensagem_erro += "   - Funciona automaticamente se Ollama estiver rodando\n\n"
    mensagem_erro += "3. Groq (GRATUITO - Muito rápido):\n"
    mensagem_erro += "   - Obtenha API key em: https://console.groq.com/\n"
    mensagem_erro += "   - Instale: pip install groq\n"
    mensagem_erro += "   - Configure: setx GROQ_API_KEY sua_chave_aqui\n\n"
    mensagem_erro += "OPÇÕES PAGAS:\n\n"
    mensagem_erro += "4. OpenAI:\n"
    mensagem_erro += "   - Obtenha API key em: https://platform.openai.com/api-keys\n"
    mensagem_erro += "   - Configure: setx OPENAI_API_KEY sua_chave_aqui\n\n"
    mensagem_erro += "5. Claude (Anthropic):\n"
    mensagem_erro += "   - Obtenha API key em: https://console.anthropic.com/\n"
    mensagem_erro += "   - Configure: setx ANTHROPIC_API_KEY sua_chave_aqui\n"
    
    if erros_detalhados:
        mensagem_erro += "\n\nDetalhes dos erros:\n"
        mensagem_erro += "\n".join(f"  - {e}" for e in erros_detalhados)
    
    raise Exception(mensagem_erro)

def _chamar_openai(prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    """Chama a API da OpenAI (GPT-4 ou GPT-3.5-turbo) com retry automático"""
    try:
        import openai
        import time
    except ImportError:
        raise Exception("Biblioteca openai não instalada. Execute: pip install openai")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não configurada. Configure a variável de ambiente OPENAI_API_KEY.")
    
    client = openai.OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Tentar com retry para rate limits
    for tentativa in range(max_retries):
        try:
            logger.info(f"🤖 Chamando OpenAI com modelo: {model} (tentativa {tentativa + 1}/{max_retries})")
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um analista especializado em trading e gestão de carteiras. Sempre responda em JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            resposta_texto = response.choices[0].message.content.strip()
            logger.debug(f"📥 Resposta OpenAI recebida: {resposta_texto[:200]}...")
            
            # Tentar extrair JSON da resposta
            json_texto = _extrair_json_da_resposta(resposta_texto)
            resultado = json.loads(json_texto)
            logger.info("✅ Resposta OpenAI parseada com sucesso")
            return resultado
            
        except openai.RateLimitError as e_rate:
            if tentativa < max_retries - 1:
                # Calcular backoff exponencial
                wait_time = (2 ** tentativa) + (time.time() % 1)  # 1s, 2s, 4s...
                logger.warning(f"⚠️  Rate limit atingido. Aguardando {wait_time:.1f}s antes de tentar novamente...")
                time.sleep(wait_time)
                continue
            else:
                raise Exception("Limite de taxa da OpenAI excedido após múltiplas tentativas. Aguarde alguns minutos e tente novamente.")
        
        except openai.APIError as e_api:
            erro_msg = str(e_api)
            logger.error(f"❌ Erro da API OpenAI: {erro_msg}")
            
            # Verificar tipo específico de erro
            if "insufficient_quota" in erro_msg.lower() or ("429" in erro_msg and "quota" in erro_msg.lower()):
                raise Exception(
                    "Cota da OpenAI insuficiente ou limite de taxa excedido.\n"
                    "Soluções:\n"
                    "1. Adicione créditos em: https://platform.openai.com/account/billing\n"
                    "2. Aguarde alguns minutos e tente novamente\n"
                    "3. Configure ANTHROPIC_API_KEY para usar Claude como alternativa"
                )
            elif "401" in erro_msg or "authentication" in erro_msg.lower():
                raise Exception("Erro de autenticação OpenAI. Verifique se a OPENAI_API_KEY está correta.")
            else:
                raise Exception(f"Erro da API OpenAI: {erro_msg}")
        
        except json.JSONDecodeError as e_json:
            logger.error(f"❌ Erro ao parsear JSON da resposta OpenAI: {e_json}")
            raise Exception(f"Erro ao processar resposta da OpenAI (JSON inválido): {str(e_json)}")
        
        except Exception as e:
            erro_msg = str(e)
            logger.error(f"❌ Erro ao chamar OpenAI: {erro_msg}")
            
            # Se for rate limit mas não foi capturado acima
            if "429" in erro_msg or "rate limit" in erro_msg.lower():
                if tentativa < max_retries - 1:
                    wait_time = (2 ** tentativa) + (time.time() % 1)
                    logger.warning(f"⚠️  Rate limit detectado. Aguardando {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("Limite de taxa excedido após múltiplas tentativas. Aguarde e tente novamente.")
            
            # Se for quota insuficiente
            if "insufficient_quota" in erro_msg.lower():
                raise Exception(
                    "Cota da OpenAI insuficiente.\n"
                    "Adicione créditos em: https://platform.openai.com/account/billing\n"
                    "Ou configure ANTHROPIC_API_KEY para usar Claude."
                )
            
            raise Exception(f"Erro ao chamar OpenAI: {erro_msg}")
    
    raise Exception("Falha ao chamar OpenAI após múltiplas tentativas.")

def _chamar_gemini(prompt: str) -> Dict[str, Any]:
    """Chama a API do Google Gemini (GRATUITO)"""
    try:
        import google.generativeai as genai
    except ImportError:
        raise Exception("Biblioteca google-generativeai não instalada. Execute: pip install google-generativeai")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não configurada. Configure a variável de ambiente GOOGLE_API_KEY.")
    
    try:
        genai.configure(api_key=api_key)
        
        # Listar modelos disponíveis e usar o primeiro que funciona
        # Ordem de preferência: gemini-1.5-flash (mais rápido), gemini-1.5-pro (mais poderoso)
        modelos_disponiveis = []
        try:
            modelos_lista = list(genai.list_models())
            modelos_disponiveis = [
                m.name for m in modelos_lista 
                if 'generateContent' in m.supported_generation_methods
                and ('flash' in m.name.lower() or 'pro' in m.name.lower())
            ]
            logger.debug(f"📋 Modelos Gemini disponíveis: {', '.join(modelos_disponiveis[:5])}")
        except Exception as e_list:
            logger.warning(f"⚠️  Não foi possível listar modelos: {e_list}")
            modelos_disponiveis = []
        
        # Ordem de tentativa: flash primeiro (mais rápido), depois pro
        modelos_tentar = ['gemini-1.5-flash', 'gemini-1.5-pro']
        if modelos_disponiveis:
            # Priorizar modelos que estão na lista de disponíveis
            modelos_tentar = [m for m in modelos_disponiveis if 'flash' in m.lower()] + \
                           [m for m in modelos_disponiveis if 'pro' in m.lower() and 'flash' not in m.lower()] + \
                           modelos_tentar
        
        modelo_usado = None
        response = None
        ultimo_erro = None
        
        for modelo_nome in modelos_tentar:
            try:
                logger.info(f"🤖 Tentando Google Gemini com modelo: {modelo_nome} (gratuito)...")
                model = genai.GenerativeModel(modelo_nome)
                
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 2000,
                    }
                )
                modelo_usado = modelo_nome
                logger.info(f"✅ Modelo {modelo_nome} funcionou!")
                break
            except Exception as e_modelo:
                ultimo_erro = str(e_modelo)
                logger.warning(f"⚠️  Modelo {modelo_nome} falhou: {ultimo_erro[:150]}")
                continue
        
        if not response:
            raise Exception(
                f"Erro ao chamar Gemini. Modelos testados: {', '.join(modelos_tentar)}\n"
                f"Último erro: {ultimo_erro}\n"
                f"Tente atualizar: pip install --upgrade google-generativeai"
            )
        
        resposta_texto = response.text.strip()
        logger.info(f"✅ Gemini ({modelo_nome}) respondeu com sucesso!")
        logger.debug(f"📥 Resposta Gemini recebida: {resposta_texto[:200]}...")
        
        json_texto = _extrair_json_da_resposta(resposta_texto)
        resultado = json.loads(json_texto)
        logger.info("✅ Resposta Gemini parseada com sucesso")
        return resultado
        
    except json.JSONDecodeError as e_json:
        logger.error(f"❌ Erro ao parsear JSON da resposta Gemini: {e_json}")
        raise Exception(f"Erro ao processar resposta da Gemini (JSON inválido): {str(e_json)}")
    except Exception as e:
        erro_msg = str(e)
        logger.error(f"❌ Erro ao chamar Gemini: {erro_msg}")
        raise Exception(f"Erro ao chamar Gemini: {erro_msg}")

def _chamar_ollama(prompt: str) -> Dict[str, Any]:
    """Chama Ollama local (100% GRATUITO)"""
    try:
        import ollama
    except ImportError:
        raise Exception("Biblioteca ollama não instalada. Execute: pip install ollama")
    
    try:
        # Verificar se Ollama está rodando
        models = ollama.list()
        if not models.get('models'):
            raise Exception("Nenhum modelo Ollama instalado. Execute: ollama pull llama2")
        
        # Tentar usar modelo disponível (preferir llama2, mistral, ou codellama)
        modelo_preferido = None
        modelos_disponiveis = [m['name'] for m in models['models']]
        
        for modelo in ['llama2', 'mistral', 'codellama', 'llama3', 'llama']:
            if any(modelo in m for m in modelos_disponiveis):
                modelo_preferido = next(m for m in modelos_disponiveis if modelo in m)
                break
        
        if not modelo_preferido:
            modelo_preferido = modelos_disponiveis[0]
        
        logger.info(f"🤖 Chamando Ollama local com modelo: {modelo_preferido} (100% gratuito)...")
        
        response = ollama.generate(
            model=modelo_preferido,
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 2000,
            }
        )
        
        resposta_texto = response['response'].strip()
        logger.debug(f"📥 Resposta Ollama recebida: {resposta_texto[:200]}...")
        
        json_texto = _extrair_json_da_resposta(resposta_texto)
        resultado = json.loads(json_texto)
        logger.info("✅ Resposta Ollama parseada com sucesso")
        return resultado
        
    except Exception as e:
        erro_msg = str(e)
        if "Connection refused" in erro_msg or "not running" in erro_msg.lower():
            raise Exception("Ollama não está rodando. Inicie o servidor Ollama primeiro.")
        logger.error(f"❌ Erro ao chamar Ollama: {erro_msg}")
        raise Exception(f"Erro ao chamar Ollama: {erro_msg}")

def _chamar_groq(prompt: str) -> Dict[str, Any]:
    """Chama a API do Groq (GRATUITO - Muito rápido)"""
    try:
        from groq import Groq
    except ImportError:
        raise Exception("Biblioteca groq não instalada. Execute: pip install groq")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não configurada. Configure a variável de ambiente GROQ_API_KEY.")
    
    try:
        client = Groq(api_key=api_key)
        
        # Usar modelo gratuito disponível
        model = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # ou "mixtral-8x7b-32768"
        
        logger.info(f"🤖 Chamando Groq com modelo: {model} (gratuito e rápido)...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um analista especializado em trading e gestão de carteiras. Sempre responda em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        resposta_texto = response.choices[0].message.content.strip()
        logger.debug(f"📥 Resposta Groq recebida: {resposta_texto[:200]}...")
        
        json_texto = _extrair_json_da_resposta(resposta_texto)
        resultado = json.loads(json_texto)
        logger.info("✅ Resposta Groq parseada com sucesso")
        return resultado
        
    except json.JSONDecodeError as e_json:
        logger.error(f"❌ Erro ao parsear JSON da resposta Groq: {e_json}")
        raise Exception(f"Erro ao processar resposta da Groq (JSON inválido): {str(e_json)}")
    except Exception as e:
        erro_msg = str(e)
        logger.error(f"❌ Erro ao chamar Groq: {erro_msg}")
        raise Exception(f"Erro ao chamar Groq: {erro_msg}")

def _chamar_claude(prompt: str) -> Dict[str, Any]:
    """Chama a API da Anthropic (Claude)"""
    try:
        from anthropic import Anthropic
    except ImportError:
        raise Exception("Biblioteca anthropic não instalada. Execute: pip install anthropic")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY não configurada. Configure a variável de ambiente ANTHROPIC_API_KEY.")
    
    try:
        client = Anthropic(api_key=api_key)
        
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        logger.info(f"🤖 Chamando Claude com modelo: {model}")
        
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        resposta_texto = response.content[0].text.strip()
        logger.debug(f"📥 Resposta Claude recebida: {resposta_texto[:200]}...")
        
        json_texto = _extrair_json_da_resposta(resposta_texto)
        resultado = json.loads(json_texto)
        logger.info("✅ Resposta Claude parseada com sucesso")
        return resultado
        
    except json.JSONDecodeError as e_json:
        logger.error(f"❌ Erro ao parsear JSON da resposta Claude: {e_json}")
        raise Exception(f"Erro ao processar resposta da Claude (JSON inválido): {str(e_json)}")
    except Exception as e:
        erro_msg = str(e)
        logger.error(f"❌ Erro ao chamar Claude: {erro_msg}")
        # Melhorar mensagem de erro comum
        if "401" in erro_msg or "authentication" in erro_msg.lower():
            raise Exception("Erro de autenticação Claude. Verifique se a ANTHROPIC_API_KEY está correta.")
        elif "rate limit" in erro_msg.lower() or "429" in erro_msg:
            raise Exception("Limite de taxa da Claude excedido. Tente novamente mais tarde.")
        else:
            raise Exception(f"Erro ao chamar Claude: {erro_msg}")

def _extrair_json_da_resposta(texto: str) -> str:
    """Extrai JSON de uma resposta que pode conter texto antes/depois."""
    # Tentar encontrar JSON entre chaves
    inicio = texto.find('{')
    fim = texto.rfind('}') + 1
    
    if inicio >= 0 and fim > inicio:
        return texto[inicio:fim]
    
    # Se não encontrar, retornar o texto original
    return texto


