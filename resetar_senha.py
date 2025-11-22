"""
Script para resetar senha de usuário
"""
import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trades.db")

def resetar_senha(email: str, nova_senha: str):
    """Reseta a senha de um usuário"""
    conn = sqlite3.connect(DB_PATH)
    try:
        # Verificar se usuário existe
        cur = conn.execute("SELECT id, email, nome FROM users WHERE email = ?", (email.lower(),))
        row = cur.fetchone()
        
        if not row:
            print(f"❌ Usuário não encontrado: {email}")
            return False
        
        user_id, user_email, user_nome = row
        print(f"✅ Usuário encontrado:")
        print(f"   ID: {user_id}")
        print(f"   Email: {user_email}")
        print(f"   Nome: {user_nome}")
        
        # Gerar novo hash da senha
        password_hash = generate_password_hash(nova_senha)
        
        # Atualizar senha
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, user_id)
        )
        conn.commit()
        
        print(f"\n✅ Senha resetada com sucesso!")
        print(f"   Nova senha: {nova_senha}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao resetar senha: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    
    email = 'vitorh.barbieri@gmail.com'
    nova_senha = 'vitor123'  # Nova senha padrão
    
    if len(sys.argv) > 1:
        nova_senha = sys.argv[1]
    
    print("="*70)
    print("🔄 RESETAR SENHA DE USUÁRIO")
    print("="*70)
    print(f"\nEmail: {email}")
    print(f"Nova senha: {nova_senha}")
    print("\n" + "="*70)
    
    sucesso = resetar_senha(email, nova_senha)
    
    if sucesso:
        print("\n" + "="*70)
        print("✅ PRONTO! Agora você pode fazer login com:")
        print(f"   Email: {email}")
        print(f"   Senha: {nova_senha}")
        print("="*70)
    else:
        print("\n❌ Falha ao resetar senha. Verifique o erro acima.")

