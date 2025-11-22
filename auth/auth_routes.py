"""
Rotas de autenticação (login, registro, logout)
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from auth.models import User, init_auth_db
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário"""
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        nome = (data.get('nome') or '').strip()
        
        if not email or not password:
            if request.is_json:
                return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
            flash('Email e senha são obrigatórios', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            if request.is_json:
                return jsonify({'erro': 'Senha deve ter pelo menos 6 caracteres'}), 400
            flash('Senha deve ter pelo menos 6 caracteres', 'error')
            return render_template('register.html')
        
        user = User.create(email, password, nome)
        if user:
            login_user(user)
            logger.info(f"✅ Novo usuário registrado: {email}")
            if request.is_json:
                return jsonify({'status': 'ok', 'mensagem': 'Usuário criado com sucesso', 'user_id': user.id})
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            if request.is_json:
                return jsonify({'erro': 'Email já está em uso'}), 400
            flash('Email já está em uso', 'error')
            return render_template('register.html')
    except Exception as e:
        logger.error(f"❌ Erro no registro: {e}")
        if request.is_json:
            return jsonify({'erro': str(e)}), 500
        flash(f'Erro ao criar conta: {str(e)}', 'error')
        return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuário"""
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        
        if not email or not password:
            if request.is_json:
                return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
            flash('Email e senha são obrigatórios', 'error')
            return render_template('login.html')
        
        user = User.get_by_email(email)
        if user and user.verify_password(password):
            if not user.is_active:
                if request.is_json:
                    return jsonify({'erro': 'Conta desativada'}), 403
                flash('Conta desativada', 'error')
                return render_template('login.html')
            
            login_user(user)
            user.update_last_login()
            logger.info(f"✅ Login realizado: {email}")
            if request.is_json:
                return jsonify({'status': 'ok', 'mensagem': 'Login realizado com sucesso', 'user_id': user.id})
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            if request.is_json:
                return jsonify({'erro': 'Email ou senha incorretos'}), 401
            flash('Email ou senha incorretos', 'error')
            return render_template('login.html')
    except Exception as e:
        logger.error(f"❌ Erro no login: {e}")
        if request.is_json:
            return jsonify({'erro': str(e)}), 500
        flash(f'Erro ao fazer login: {str(e)}', 'error')
        return render_template('login.html')

@auth_bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """Logout de usuário"""
    logger.info(f"✅ Logout realizado: {current_user.email}")
    logout_user()
    if request.is_json:
        return jsonify({'status': 'ok', 'mensagem': 'Logout realizado com sucesso'})
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    """Retorna informações do usuário atual"""
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'nome': current_user.nome,
        'is_admin': current_user.is_admin
    })

