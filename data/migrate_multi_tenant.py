"""
Script de migração para adicionar suporte multi-tenant
Adiciona user_id nas tabelas trades e dividendos
"""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trades.db")

def migrate():
    """Migra banco de dados para multi-tenant"""
    print("="*70)
    print("🔄 Migração para Multi-Tenant")
    print("="*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Criar tabela users se não existir
        print("\n1. Criando tabela users...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT,
                is_active INTEGER DEFAULT 1,
                is_admin INTEGER DEFAULT 0
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)")
        print("✅ Tabela users criada")
        
        # 2. Verificar se user_id já existe em trades
        print("\n2. Verificando tabela trades...")
        cursor.execute("PRAGMA table_info(trades)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("   Adicionando coluna user_id em trades...")
            cursor.execute("ALTER TABLE trades ADD COLUMN user_id INTEGER DEFAULT 1")
            print("✅ Coluna user_id adicionada em trades")
            
            # Migrar dados existentes para user_id=1
            print("   Migrando dados existentes para user_id=1...")
            cursor.execute("UPDATE trades SET user_id = 1 WHERE user_id IS NULL")
            print("✅ Dados migrados")
        else:
            print("✅ Coluna user_id já existe em trades")
        
        # 3. Verificar se user_id já existe em dividendos
        print("\n3. Verificando tabela dividendos...")
        cursor.execute("PRAGMA table_info(dividendos)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("   Adicionando coluna user_id em dividendos...")
            cursor.execute("ALTER TABLE dividendos ADD COLUMN user_id INTEGER DEFAULT 1")
            print("✅ Coluna user_id adicionada em dividendos")
            
            # Migrar dados existentes para user_id=1
            print("   Migrando dados existentes para user_id=1...")
            cursor.execute("UPDATE dividendos SET user_id = 1 WHERE user_id IS NULL")
            print("✅ Dados migrados")
        else:
            print("✅ Coluna user_id já existe em dividendos")
        
        # 4. Criar índices para performance
        print("\n4. Criando índices...")
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_user_ticker ON trades (user_id, ticker)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_user_date ON trades (user_id, trade_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dividendos_user_ticker ON dividendos (user_id, ticker)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dividendos_user_data ON dividendos (user_id, data_pagamento)")
            print("✅ Índices criados")
        except Exception as e:
            print(f"⚠️  Alguns índices podem já existir: {e}")
        
        # 5. Criar usuário padrão se não existir
        print("\n5. Criando usuário padrão...")
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            from werkzeug.security import generate_password_hash
            password_hash = generate_password_hash("admin123")
            cursor.execute("""
                INSERT INTO users (email, password_hash, nome, is_admin) 
                VALUES (?, ?, ?, ?)
            """, ("admin@algoritimo.com", password_hash, "Administrador", 1))
            print("✅ Usuário padrão criado:")
            print("   Email: admin@algoritimo.com")
            print("   Senha: admin123")
        else:
            print("✅ Usuários já existem")
        
        conn.commit()
        print("\n" + "="*70)
        print("✅ Migração concluída com sucesso!")
        print("="*70)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Erro na migração: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()

