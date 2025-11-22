"""
Orquestrador de sinais: combina sinais de múltiplas estratégias
Gera sinal final usando pesos configuráveis
"""
import pandas as pd
import numpy as np
from typing import Dict


class SignalOrchestrator:
    """
    Combina sinais de múltiplas estratégias em um sinal final
    """
    
    def __init__(self, pesos: Dict[str, float] = None):
        """
        Args:
            pesos: Dicionário com pesos de cada estratégia
                  Ex: {'trend': 0.4, 'reversao': 0.3, 'news': 0.3}
        """
        if pesos is None:
            pesos = {
                'trend': 0.4,
                'reversao': 0.3,
                'news': 0.3
            }
        
        # Normalizar pesos para somar 1.0
        total = sum(pesos.values())
        self.pesos = {k: v/total for k, v in pesos.items()}
    
    def combinar_sinais(
        self,
        sinal_trend: pd.Series = None,
        sinal_reversao: pd.Series = None,
        sinal_news: pd.Series = None
    ) -> pd.Series:
        """
        Combina sinais individuais em sinal final
        
        Args:
            sinal_trend: Sinais da estratégia de tendência
            sinal_reversao: Sinais da estratégia de reversão
            sinal_news: Sinais da estratégia de notícias
        
        Returns:
            Series com sinal final combinado (-1, 0, +1)
        """
        sinais = {}
        
        if sinal_trend is not None:
            sinais['trend'] = sinal_trend
        
        if sinal_reversao is not None:
            sinais['reversao'] = sinal_reversao
        
        if sinal_news is not None:
            sinais['news'] = sinal_news
        
        if not sinais:
            return pd.Series(0, index=pd.DatetimeIndex([]))
        
        # Encontrar índice comum
        indices = [s.index for s in sinais.values()]
        indice_comum = indices[0]
        for idx in indices[1:]:
            indice_comum = indice_comum.intersection(idx)
        
        if len(indice_comum) == 0:
            return pd.Series(0, index=pd.DatetimeIndex([]))
        
        # Combinar sinais com pesos
        sinal_final = pd.Series(0.0, index=indice_comum)
        
        for estrategia, sinal in sinais.items():
            if estrategia in self.pesos:
                peso = self.pesos[estrategia]
                sinal_alinhado = sinal.reindex(indice_comum, fill_value=0)
                sinal_final += sinal_alinhado * peso
        
        # Converter para sinal discreto
        sinal_discreto = pd.Series(0, index=sinal_final.index)
        sinal_discreto[sinal_final > 0.3] = 1   # Compra
        sinal_discreto[sinal_final < -0.3] = -1  # Venda
        # Entre -0.3 e 0.3 fica neutro (0)
        
        return sinal_discreto
    
    def calcular_confianca(
        self,
        sinal_trend: pd.Series = None,
        sinal_reversao: pd.Series = None,
        sinal_news: pd.Series = None
    ) -> pd.Series:
        """
        Calcula confiança do sinal final baseado em concordância entre estratégias
        
        Args:
            sinal_trend: Sinais da estratégia de tendência
            sinal_reversao: Sinais da estratégia de reversão
            sinal_news: Sinais da estratégia de notícias
        
        Returns:
            Series com confiança (0 a 1)
        """
        sinais = {}
        
        if sinal_trend is not None:
            sinais['trend'] = sinal_trend
        
        if sinal_reversao is not None:
            sinais['reversao'] = sinal_reversao
        
        if sinal_news is not None:
            sinais['news'] = sinal_news
        
        if len(sinais) < 2:
            return pd.Series(0.5, index=pd.DatetimeIndex([]))
        
        # Encontrar índice comum
        indices = [s.index for s in sinais.values()]
        indice_comum = indices[0]
        for idx in indices[1:]:
            indice_comum = indice_comum.intersection(idx)
        
        if len(indice_comum) == 0:
            return pd.Series(0.5, index=pd.DatetimeIndex([]))
        
        # Calcular concordância
        confianca = pd.Series(0.0, index=indice_comum)
        
        sinais_alinhados = {}
        for nome, sinal in sinais.items():
            sinais_alinhados[nome] = sinal.reindex(indice_comum, fill_value=0)
        
        # Contar quantas estratégias concordam
        for idx in indice_comum:
            valores = [sinais_alinhados[nome][idx] for nome in sinais_alinhados]
            valores_abs = [abs(v) for v in valores]
            
            # Se todas têm o mesmo sinal (todas compra ou todas venda)
            if len(set([v for v in valores if v != 0])) == 1:
                confianca[idx] = 1.0
            # Se há discordância
            elif sum(valores_abs) > 0:
                # Confiança proporcional à concordância
                sinal_medio = np.mean([v for v in valores if v != 0] or [0])
                confianca[idx] = abs(sinal_medio)
            else:
                confianca[idx] = 0.3  # Baixa confiança quando neutro
        
        return confianca


if __name__ == "__main__":
    # Teste
    print("Testando orquestrador de sinais...")
    
    import pandas as pd
    
    dates = pd.date_range('2025-01-01', periods=10, freq='D')
    
    sinal_trend = pd.Series([0, 1, 1, 0, -1, -1, 0, 1, 0, 0], index=dates)
    sinal_reversao = pd.Series([1, 0, 0, -1, 0, 0, 1, 0, -1, 0], index=dates)
    sinal_news = pd.Series([0, 1, 0, 0, -1, 0, 1, 1, 0, 0], index=dates)
    
    orchestrator = SignalOrchestrator()
    sinal_final = orchestrator.combinar_sinais(sinal_trend, sinal_reversao, sinal_news)
    confianca = orchestrator.calcular_confianca(sinal_trend, sinal_reversao, sinal_news)
    
    print(f"\nSinal final:")
    print(sinal_final)
    print(f"\nConfiança:")
    print(confianca)










