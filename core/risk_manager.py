"""
Gestão de risco: stop-loss, take-profit, tamanho de posição
"""
import pandas as pd
import numpy as np
from typing import Optional


class RiskManager:
    """
    Gerencia risco das operações
    """
    
    def __init__(
        self,
        risco_por_trade: float = 0.02,  # 2% da banca por trade
        stop_loss_atr_multiplier: float = 2.0,
        take_profit_atr_multiplier: float = 3.0,
        max_posicao: float = 0.1  # Máximo 10% da banca em uma posição
    ):
        """
        Args:
            risco_por_trade: Percentual da banca a arriscar por trade
            stop_loss_atr_multiplier: Multiplicador do ATR para stop-loss
            take_profit_atr_multiplier: Multiplicador do ATR para take-profit
            max_posicao: Tamanho máximo de posição (fração da banca)
        """
        self.risco_por_trade = risco_por_trade
        self.stop_loss_atr_multiplier = stop_loss_atr_multiplier
        self.take_profit_atr_multiplier = take_profit_atr_multiplier
        self.max_posicao = max_posicao
    
    def calcular_stop_loss(
        self,
        preco_entrada: float,
        sinal: int,  # +1 para compra, -1 para venda
        atr: float
    ) -> float:
        """
        Calcula preço de stop-loss baseado em ATR
        
        Args:
            preco_entrada: Preço de entrada da operação
            sinal: Direção da operação (+1 compra, -1 venda)
            atr: Valor do ATR
        
        Returns:
            Preço de stop-loss
        """
        distancia_stop = atr * self.stop_loss_atr_multiplier
        
        if sinal == 1:  # Compra
            stop_loss = preco_entrada - distancia_stop
        else:  # Venda
            stop_loss = preco_entrada + distancia_stop
        
        return stop_loss
    
    def calcular_take_profit(
        self,
        preco_entrada: float,
        sinal: int,
        atr: float
    ) -> float:
        """
        Calcula preço de take-profit baseado em ATR
        
        Args:
            preco_entrada: Preço de entrada
            sinal: Direção da operação
            atr: Valor do ATR
        
        Returns:
            Preço de take-profit
        """
        distancia_tp = atr * self.take_profit_atr_multiplier
        
        if sinal == 1:  # Compra
            take_profit = preco_entrada + distancia_tp
        else:  # Venda
            take_profit = preco_entrada - distancia_tp
        
        return take_profit
    
    def calcular_tamanho_posicao(
        self,
        banca: float,
        preco_entrada: float,
        stop_loss: float,
        sinal: int
    ) -> int:
        """
        Calcula tamanho da posição baseado no risco
        
        Args:
            banca: Capital disponível
            preco_entrada: Preço de entrada
            stop_loss: Preço de stop-loss
            sinal: Direção da operação
        
        Returns:
            Quantidade de ações/contratos
        """
        # Risco máximo por trade
        risco_maximo = banca * self.risco_por_trade
        
        # Distância até stop-loss
        if sinal == 1:  # Compra
            distancia_stop = preco_entrada - stop_loss
        else:  # Venda
            distancia_stop = stop_loss - preco_entrada
        
        if distancia_stop <= 0:
            return 0
        
        # Quantidade baseada no risco
        quantidade = int(risco_maximo / distancia_stop)
        
        # Limitar pelo máximo de posição
        valor_maximo_posicao = banca * self.max_posicao
        quantidade_maxima = int(valor_maximo_posicao / preco_entrada)
        
        quantidade = min(quantidade, quantidade_maxima)
        
        return max(0, quantidade)
    
    def verificar_stop_loss_take_profit(
        self,
        preco_atual: float,
        preco_entrada: float,
        stop_loss: float,
        take_profit: float,
        sinal: int
    ) -> Optional[str]:
        """
        Verifica se stop-loss ou take-profit foram atingidos
        
        Args:
            preco_atual: Preço atual do ativo
            preco_entrada: Preço de entrada
            stop_loss: Preço de stop-loss
            take_profit: Preço de take-profit
            sinal: Direção da operação
        
        Returns:
            'stop_loss', 'take_profit' ou None
        """
        if sinal == 1:  # Compra
            if preco_atual <= stop_loss:
                return 'stop_loss'
            elif preco_atual >= take_profit:
                return 'take_profit'
        else:  # Venda
            if preco_atual >= stop_loss:
                return 'stop_loss'
            elif preco_atual <= take_profit:
                return 'take_profit'
        
        return None


if __name__ == "__main__":
    # Teste
    print("Testando gestão de risco...")
    
    risk_manager = RiskManager()
    
    preco_entrada = 25.0
    atr = 0.5
    banca = 10000.0
    sinal = 1  # Compra
    
    stop_loss = risk_manager.calcular_stop_loss(preco_entrada, sinal, atr)
    take_profit = risk_manager.calcular_take_profit(preco_entrada, sinal, atr)
    quantidade = risk_manager.calcular_tamanho_posicao(banca, preco_entrada, stop_loss, sinal)
    
    print(f"\nPreço entrada: R$ {preco_entrada:.2f}")
    print(f"Stop-loss: R$ {stop_loss:.2f}")
    print(f"Take-profit: R$ {take_profit:.2f}")
    print(f"Quantidade: {quantidade} ações")
    print(f"Valor da posição: R$ {quantidade * preco_entrada:.2f}")









