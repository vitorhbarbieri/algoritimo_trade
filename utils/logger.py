"""
Sistema de logging padronizado
Níveis: DEBUG, INFO, WARNING, ERROR
"""
import logging
from datetime import datetime
from typing import Optional


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('algoritimo_trade')


def log_debug(mensagem: str):
    """Log de debug"""
    logger.debug(mensagem)


def log_info(mensagem: str):
    """Log de informação"""
    logger.info(mensagem)


def log_warning(mensagem: str):
    """Log de aviso"""
    logger.warning(mensagem)


def log_error(mensagem: str):
    """Log de erro"""
    logger.error(mensagem)


def log_trade(tipo: str, ticker: str, quantidade: int, preco: float, valor_total: float):
    """
    Log específico para operações de trade
    
    Args:
        tipo: 'COMPRA' ou 'VENDA'
        ticker: Código do ativo
        quantidade: Quantidade
        preco: Preço
        valor_total: Valor total da operação
    """
    emoji = "🟢" if tipo == "COMPRA" else "🔴"
    log_info(f"{emoji} {tipo}: {quantidade} x {ticker} @ R$ {preco:.2f} = R$ {valor_total:.2f}")


def log_sinal(ticker: str, sinal: int, confianca: float = None):
    """
    Log específico para sinais gerados
    
    Args:
        ticker: Código do ativo
        sinal: Sinal (-1, 0, +1)
        confianca: Confiança do sinal (0 a 1)
    """
    sinal_str = "COMPRA" if sinal == 1 else "VENDA" if sinal == -1 else "NEUTRO"
    confianca_str = f" (confiança: {confianca:.2%})" if confianca is not None else ""
    log_info(f"📊 {ticker}: {sinal_str}{confianca_str}")


if __name__ == "__main__":
    # Teste
    print("Testando logger...")
    
    log_debug("Mensagem de debug")
    log_info("Mensagem de informação")
    log_warning("Mensagem de aviso")
    log_error("Mensagem de erro")
    log_trade("COMPRA", "ITUB4", 100, 25.50, 2550.0)
    log_sinal("ITUB4", 1, 0.75)

