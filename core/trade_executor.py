"""
Executor de trades: estrutura para execução (mock por enquanto)
Interface para futura integração com corretoras via API
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from utils.logger import log_info, log_error, log_warning


class TradeExecutor:
    """
    Executa operações de compra e venda
    Por enquanto é mock, mas preparado para integração com corretoras
    """
    
    def __init__(self, modo_mock: bool = True):
        """
        Args:
            modo_mock: Se True, apenas simula execução (padrão)
        """
        self.modo_mock = modo_mock
        self.historico_operacoes = []
        self.posicoes_abertas = {}
    
    def executar_compra(
        self,
        ticker: str,
        quantidade: int,
        preco: float,
        timestamp: datetime = None
    ) -> Dict:
        """
        Executa ordem de compra
        
        Args:
            ticker: Código do ativo
            quantidade: Quantidade a comprar
            preco: Preço de compra
            timestamp: Data/hora da operação
        
        Returns:
            Dicionário com detalhes da operação
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        operacao = {
            'tipo': 'COMPRA',
            'ticker': ticker,
            'quantidade': quantidade,
            'preco': preco,
            'valor_total': quantidade * preco,
            'timestamp': timestamp,
            'status': 'EXECUTADA' if self.modo_mock else 'PENDENTE'
        }
        
        if self.modo_mock:
            log_info(f"🟢 COMPRA: {quantidade} x {ticker} @ R$ {preco:.2f} = R$ {operacao['valor_total']:.2f}")
        else:
            # Aqui seria a chamada real à API da corretora
            log_warning(f"Modo real não implementado ainda")
            operacao['status'] = 'ERRO'
        
        self.historico_operacoes.append(operacao)
        
        # Atualizar posições abertas
        if ticker in self.posicoes_abertas:
            posicao = self.posicoes_abertas[ticker]
            # Média ponderada
            total_quantidade = posicao['quantidade'] + quantidade
            total_valor = (posicao['preco_medio'] * posicao['quantidade']) + operacao['valor_total']
            posicao['quantidade'] = total_quantidade
            posicao['preco_medio'] = total_valor / total_quantidade
        else:
            self.posicoes_abertas[ticker] = {
                'quantidade': quantidade,
                'preco_medio': preco,
                'timestamp_abertura': timestamp
            }
        
        return operacao
    
    def executar_venda(
        self,
        ticker: str,
        quantidade: int,
        preco: float,
        timestamp: datetime = None
    ) -> Dict:
        """
        Executa ordem de venda
        
        Args:
            ticker: Código do ativo
            quantidade: Quantidade a vender
            preco: Preço de venda
            timestamp: Data/hora da operação
        
        Returns:
            Dicionário com detalhes da operação
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Verificar se há posição aberta
        if ticker not in self.posicoes_abertas:
            log_error(f"Tentativa de vender {ticker} sem posição aberta")
            return {
                'tipo': 'VENDA',
                'ticker': ticker,
                'status': 'ERRO',
                'erro': 'Sem posição aberta'
            }
        
        posicao = self.posicoes_abertas[ticker]
        quantidade_disponivel = posicao['quantidade']
        
        if quantidade > quantidade_disponivel:
            log_warning(f"Tentativa de vender {quantidade} mas só há {quantidade_disponivel}")
            quantidade = quantidade_disponivel
        
        operacao = {
            'tipo': 'VENDA',
            'ticker': ticker,
            'quantidade': quantidade,
            'preco': preco,
            'valor_total': quantidade * preco,
            'preco_medio_compra': posicao['preco_medio'],
            'lucro_prejuizo': (preco - posicao['preco_medio']) * quantidade,
            'timestamp': timestamp,
            'status': 'EXECUTADA' if self.modo_mock else 'PENDENTE'
        }
        
        if self.modo_mock:
            lucro_str = f"Lucro: R$ {operacao['lucro_prejuizo']:.2f}" if operacao['lucro_prejuizo'] > 0 else f"Prejuízo: R$ {abs(operacao['lucro_prejuizo']):.2f}"
            log_info(f"🔴 VENDA: {quantidade} x {ticker} @ R$ {preco:.2f} = R$ {operacao['valor_total']:.2f} | {lucro_str}")
        else:
            log_warning(f"Modo real não implementado ainda")
            operacao['status'] = 'ERRO'
        
        self.historico_operacoes.append(operacao)
        
        # Atualizar posições abertas
        posicao['quantidade'] -= quantidade
        if posicao['quantidade'] <= 0:
            del self.posicoes_abertas[ticker]
        
        return operacao
    
    def obter_historico(self) -> pd.DataFrame:
        """
        Retorna histórico de operações como DataFrame
        
        Returns:
            DataFrame com histórico
        """
        if not self.historico_operacoes:
            return pd.DataFrame()
        
        return pd.DataFrame(self.historico_operacoes)
    
    def obter_posicoes_abertas(self) -> Dict:
        """
        Retorna posições abertas
        
        Returns:
            Dicionário com posições abertas
        """
        return self.posicoes_abertas.copy()


if __name__ == "__main__":
    # Teste
    print("Testando executor de trades...")
    
    executor = TradeExecutor(modo_mock=True)
    
    # Simular algumas operações
    executor.executar_compra("ITUB4", 100, 25.50)
    executor.executar_compra("ITUB4", 50, 26.00)
    executor.executar_venda("ITUB4", 75, 27.00)
    
    print(f"\nHistórico:")
    print(executor.obter_historico())
    print(f"\nPosições abertas:")
    print(executor.obter_posicoes_abertas())









