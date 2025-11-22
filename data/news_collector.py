"""
Coletor de notícias via RSS e web scraping
Retorna dados estruturados de notícias financeiras
"""
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
from typing import List, Dict
import time


def coletar_noticias_rss(url_rss: str) -> List[Dict]:
    """
    Coleta notícias de um feed RSS
    
    Args:
        url_rss: URL do feed RSS
    
    Returns:
        Lista de dicionários com: titulo, resumo, link, data, fonte
    """
    noticias = []
    
    try:
        feed = feedparser.parse(url_rss)
        
        for entry in feed.entries:
            noticia = {
                'titulo': entry.get('title', ''),
                'resumo': entry.get('summary', entry.get('description', '')),
                'link': entry.get('link', ''),
                'data': entry.get('published', ''),
                'fonte': feed.feed.get('title', 'RSS'),
                'timestamp': datetime.now()
            }
            noticias.append(noticia)
    
    except Exception as e:
        print(f"Erro ao coletar RSS de {url_rss}: {e}")
    
    return noticias


def coletar_noticias_web(site: str, url: str, tag: str = 'a', class_name: str = None) -> List[Dict]:
    """
    Coleta notícias via web scraping
    
    Args:
        site: Nome do site
        url: URL da página
        tag: Tag HTML para buscar
        class_name: Classe CSS para filtrar
    
    Returns:
        Lista de dicionários com notícias
    """
    noticias = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if class_name:
            elementos = soup.find_all(tag, class_=class_name)
        else:
            elementos = soup.find_all(tag, href=True)
        
        for elemento in elementos[:20]:  # Limitar a 20 notícias
            titulo = elemento.get_text().strip()
            link = elemento.get('href', '')
            
            if not titulo or len(titulo) < 20:
                continue
            
            if not link.startswith('http'):
                if 'globo.com' in url:
                    link = f"https://{site}.globo.com{link}" if link.startswith('/') else link
                elif 'uol.com.br' in url:
                    link = f"https://{site}.uol.com.br{link}" if link.startswith('/') else link
            
            noticia = {
                'titulo': titulo,
                'resumo': '',
                'link': link,
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'fonte': site,
                'timestamp': datetime.now()
            }
            noticias.append(noticia)
            
            if len(noticias) >= 15:
                break
    
    except Exception as e:
        print(f"Erro ao coletar notícias de {site}: {e}")
    
    return noticias


def coletar_noticias_brasileiras() -> List[Dict]:
    """
    Coleta notícias de sites brasileiros de economia
    
    Returns:
        Lista consolidada de notícias
    """
    todas_noticias = []
    
    # Sites brasileiros
    sites = {
        'g1': {
            'url': 'https://g1.globo.com/economia/',
            'tag': 'a',
            'class_name': 'feed-post-link'
        },
        'valor': {
            'url': 'https://valor.globo.com/',
            'tag': 'a',
            'class_name': 'bstn-dedupe-url'
        },
        'folha': {
            'url': 'https://www1.folha.uol.com.br/mercado/',
            'tag': 'a',
            'class_name': 'c-headline__url'
        }
    }
    
    for site, config in sites.items():
        try:
            noticias = coletar_noticias_web(
                site,
                config['url'],
                config['tag'],
                config['class_name']
            )
            todas_noticias.extend(noticias)
            time.sleep(0.5)  # Delay entre requisições
        except Exception as e:
            print(f"Erro ao coletar de {site}: {e}")
            continue
    
    return todas_noticias


if __name__ == "__main__":
    # Teste
    print("Testando coletor de notícias...")
    noticias = coletar_noticias_brasileiras()
    print(f"\nNotícias coletadas: {len(noticias)}")
    if noticias:
        print(f"\nPrimeira notícia:")
        print(f"Título: {noticias[0]['titulo']}")
        print(f"Fonte: {noticias[0]['fonte']}")









