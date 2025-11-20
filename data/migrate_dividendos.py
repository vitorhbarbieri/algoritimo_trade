"""
Script de migração para adicionar colunas na tabela dividendos
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trades.db")

def migrate():
    """Adiciona colunas se não existirem"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(dividendos)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'data_busca' not in columns:
            print("➕ Adicionando coluna 'data_busca'...")
            cursor.execute("ALTER TABLE dividendos ADD COLUMN data_busca TEXT")
            print("✅ Coluna 'data_busca' adicionada")
        else:
            print("ℹ️  Coluna 'data_busca' já existe")
        
        if 'fonte' not in columns:
            print("➕ Adicionando coluna 'fonte'...")
            cursor.execute("ALTER TABLE dividendos ADD COLUMN fonte TEXT DEFAULT 'brapi.dev'")
            print("✅ Coluna 'fonte' adicionada")
        else:
            print("ℹ️  Coluna 'fonte' já existe")
        
        if 'data_ex_dividendo' not in columns:
            print("➕ Adicionando coluna 'data_ex_dividendo'...")
            cursor.execute("ALTER TABLE dividendos ADD COLUMN data_ex_dividendo TEXT")
            print("✅ Coluna 'data_ex_dividendo' adicionada")
        else:
            print("ℹ️  Coluna 'data_ex_dividendo' já existe")
        
        # Verificar se o índice existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_dividendos_data_busca'")
        if not cursor.fetchone():
            print("➕ Criando índice 'idx_dividendos_data_busca'...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dividendos_data_busca ON dividendos (data_busca)")
            print("✅ Índice criado")
        else:
            print("ℹ️  Índice já existe")
        
        # Criar índice para data_ex_dividendo
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_dividendos_data_ex'")
        if not cursor.fetchone():
            print("➕ Criando índice 'idx_dividendos_data_ex'...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dividendos_data_ex ON dividendos (data_ex_dividendo)")
            print("✅ Índice criado")
        else:
            print("ℹ️  Índice já existe")
        
        conn.commit()
        print("✅ Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Iniciando migração do banco de dados...")
    migrate()

