"""
Modelos de usuário e autenticação
"""
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trades.db")

@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_auth_db():
    """Inicializa tabelas de autenticação"""
    with _connect() as conn:
        conn.execute("""
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
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)")

class User(UserMixin):
    """Modelo de usuário para Flask-Login"""
    
    def __init__(self, id, email, nome=None, is_active=True, is_admin=False):
        self.id = id
        self.email = email
        self.nome = nome or email.split('@')[0]
        # Definir is_active e is_admin como atributos simples (não propriedades)
        # Isso evita conflitos com Flask-Login que pode tentar definir como propriedade
        self._is_active = bool(is_active)
        self._is_admin = bool(is_admin)
    
    @property
    def is_active(self):
        """Propriedade is_active para Flask-Login"""
        return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        """Setter para is_active"""
        self._is_active = bool(value)
    
    @property
    def is_admin(self):
        """Propriedade is_admin"""
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        """Setter para is_admin"""
        self._is_admin = bool(value)
    
    @staticmethod
    def get(user_id):
        """Busca usuário por ID"""
        with _connect() as conn:
            row = conn.execute(
                "SELECT id, email, nome, is_active, is_admin FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    nome=row['nome'],
                    is_active=row['is_active'],
                    is_admin=row['is_admin']
                )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Busca usuário por email"""
        with _connect() as conn:
            row = conn.execute(
                "SELECT id, email, nome, is_active, is_admin FROM users WHERE email = ?",
                (email.lower(),)
            ).fetchone()
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    nome=row['nome'],
                    is_active=row['is_active'],
                    is_admin=row['is_admin']
                )
        return None
    
    @staticmethod
    def create(email, password, nome=None):
        """Cria novo usuário"""
        email = email.lower().strip()
        password_hash = generate_password_hash(password)
        
        with _connect() as conn:
            try:
                cursor = conn.execute(
                    """INSERT INTO users (email, password_hash, nome) 
                       VALUES (?, ?, ?)""",
                    (email, password_hash, nome or email.split('@')[0])
                )
                user_id = cursor.lastrowid
                return User.get(user_id)
            except sqlite3.IntegrityError:
                return None  # Email já existe
    
    def verify_password(self, password):
        """Verifica senha"""
        with _connect() as conn:
            row = conn.execute(
                "SELECT password_hash FROM users WHERE id = ?",
                (self.id,)
            ).fetchone()
            if row:
                return check_password_hash(row['password_hash'], password)
        return False
    
    def update_last_login(self):
        """Atualiza último login"""
        with _connect() as conn:
            conn.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now().isoformat(), self.id)
            )

