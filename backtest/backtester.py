"""
Backtester: simula estratégias sobre dados históricos
Calcula métricas: retorno total, drawdown, Sharpe ratio
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from core.risk_manager import RiskManager
from core.trade_executor import TradeExecutor


class Backtester:
    """
    Executa backtest de estratégias
    """
    
    def __init__(
        self,
        capital_inicial: float = 10000.0,
        risco_por_trade: float = 0.02
    ):
        """
        Args:
            capital_inicial: Capital inicial para backtest
            risco_por_trade: Risco por trade (padrão: 2%)
        """
        self.capital_inicial = capital_inicial
        self.risk_manager = RiskManager(risco_por_trade=risco_por_trade)
        self.executor = TradeExecutor(modo_mock=True)
    
    def executar_backtest(
        self,
        df: pd.DataFrame,
        sinais: pd.Series,
        ticker: str = "ATIVO"
    ) -> Dict:
        """
        Executa backtest completo
        
        Args:
            df: DataFrame com dados OHLCV e indicadores
            sinais: Series com sinais de entrada/saída (+1, 0, -1)
            ticker: Código do ativo
        
        Returns:
            Dicionário com resultados do backtest
        """
        capital = self.capital_inicial
        posicao_aberta = False
        preco_entrada = 0.0
        quantidade = 0
        stop_loss = 0.0
        take_profit = 0.0
        sinal_entrada = 0
        
        resultados = []
        equity_curve = [capital]
        
        for i, (timestamp, row) in enumerate(df.iterrows()):
            preco_atual = row['Close']
            atr = row.get('ATR', preco_atual * 0.02)  # Fallback se não tiver ATR
            
            sinal = sinais.get(timestamp, 0)
            
            # Verificar stop-loss ou take-profit se houver posição aberta
            if posicao_aberta:
                resultado = self.risk_manager.verificar_stop_loss_take_profit(
                    preco_atual, preco_entrada, stop_loss, take_profit, sinal_entrada
                )
                
                if resultado == 'stop_loss':
                    # Fechar posição no stop-loss
                    operacao = self.executor.executar_venda(
                        ticker, quantidade, stop_loss, timestamp
                    )
                    lucro_prejuizo = operacao.get('lucro_prejuizo', 0)
                    capital += operacao['valor_total'] + lucro_prejuizo
                    posicao_aberta = False
                    resultados.append({
                        'timestamp': timestamp,
                        'acao': 'STOP_LOSS',
                        'preco': stop_loss,
                        'lucro_prejuizo': lucro_prejuizo
                    })
                
                elif resultado == 'take_profit':
                    # Fechar posição no take-profit
                    operacao = self.executor.executar_venda(
                        ticker, quantidade, take_profit, timestamp
                    )
                    lucro_prejuizo = operacao.get('lucro_prejuizo', 0)
                    capital += operacao['valor_total'] + lucro_prejuizo
                    posicao_aberta = False
                    resultados.append({
                        'timestamp': timestamp,
                        'acao': 'TAKE_PROFIT',
                        'preco': take_profit,
                        'lucro_prejuizo': lucro_prejuizo
                    })
            
            # Entrar em nova posição
            if not posicao_aberta and sinal != 0:
                preco_entrada = preco_atual
                sinal_entrada = sinal
                stop_loss = self.risk_manager.calcular_stop_loss(
                    preco_entrada, sinal_entrada, atr
                )
                take_profit = self.risk_manager.calcular_take_profit(
                    preco_entrada, sinal_entrada, atr
                )
                quantidade = self.risk_manager.calcular_tamanho_posicao(
                    capital, preco_entrada, stop_loss, sinal_entrada
                )
                
                if quantidade > 0:
                    operacao = self.executor.executar_compra(
                        ticker, quantidade, preco_entrada, timestamp
                    )
                    capital -= operacao['valor_total']
                    posicao_aberta = True
                    resultados.append({
                        'timestamp': timestamp,
                        'acao': 'ENTRADA',
                        'preco': preco_entrada,
                        'quantidade': quantidade,
                        'sinal': sinal_entrada
                    })
            
            # Fechar posição se sinal mudar
            elif posicao_aberta and sinal != 0 and sinal != sinal_entrada:
                operacao = self.executor.executar_venda(
                    ticker, quantidade, preco_atual, timestamp
                )
                lucro_prejuizo = operacao.get('lucro_prejuizo', 0)
                capital += operacao['valor_total'] + lucro_prejuizo
                posicao_aberta = False
                resultados.append({
                    'timestamp': timestamp,
                    'acao': 'SAIDA_SINAL',
                    'preco': preco_atual,
                    'lucro_prejuizo': lucro_prejuizo
                })
            
            # Atualizar equity curve
            if posicao_aberta:
                valor_posicao = quantidade * preco_atual
                capital_atual = capital + valor_posicao
            else:
                capital_atual = capital
            
            equity_curve.append(capital_atual)
        
        # Fechar posição final se houver
        if posicao_aberta:
            ultima_linha = df.iloc[-1]
            preco_final = ultima_linha['Close']
            operacao = self.executor.executar_venda(
                ticker, quantidade, preco_final, df.index[-1]
            )
            lucro_prejuizo = operacao.get('lucro_prejuizo', 0)
            capital += operacao['valor_total'] + lucro_prejuizo
        
        # Calcular métricas
        equity_series = pd.Series(equity_curve)
        retorno_total = (capital - self.capital_inicial) / self.capital_inicial
        
        # Drawdown
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Sharpe ratio (simplificado)
        retornos_diarios = equity_series.pct_change().dropna()
        if len(retornos_diarios) > 0 and retornos_diarios.std() > 0:
            sharpe = (retornos_diarios.mean() / retornos_diarios.std()) * np.sqrt(252)
        else:
            sharpe = 0.0
        
        # Estatísticas de trades
        trades_lucrativos = [r for r in resultados if r.get('lucro_prejuizo', 0) > 0]
        trades_prejuizo = [r for r in resultados if r.get('lucro_prejuizo', 0) < 0]
        
        win_rate = len(trades_lucrativos) / len([r for r in resultados if 'lucro_prejuizo' in r]) if resultados else 0
        
        return {
            'capital_final': capital,
            'retorno_total': retorno_total,
            'retorno_percentual': retorno_total * 100,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'num_trades': len([r for r in resultados if r.get('acao') in ['ENTRADA', 'STOP_LOSS', 'TAKE_PROFIT']]),
            'win_rate': win_rate,
            'trades_lucrativos': len(trades_lucrativos),
            'trades_prejuizo': len(trades_prejuizo),
            'equity_curve': equity_series,
            'resultados': resultados
        }


if __name__ == "__main__":
    # Teste
    print("Testando backtester...")
    
    import yfinance as yf
    from features.technical_indicators import calcular_todos_indicadores
    from strategies.trend_strategy import gerar_sinal_tendencia
    
    dados = yf.download("ITUB4.SA", period="6mo", progress=False)
    
    if not dados.empty:
        df = calcular_todos_indicadores(dados)
        sinais = gerar_sinal_tendencia(df)
        
        backtester = Backtester()
        resultados = backtester.executar_backtest(df, sinais, "ITUB4.SA")
        
        print(f"\nResultados do backtest:")
        print(f"Retorno total: {resultados['retorno_percentual']:.2f}%")
        print(f"Max drawdown: {resultados['max_drawdown']:.2%}")
        print(f"Sharpe ratio: {resultados['sharpe_ratio']:.2f}")
        print(f"Win rate: {resultados['win_rate']:.2%}")










