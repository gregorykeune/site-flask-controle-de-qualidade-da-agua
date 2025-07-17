# user_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import get_flashed_messages
from models.iot.user import User, Role
from models.db import db
from controller.app_controller import login_manager


user_bp = Blueprint('user_bp', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_bp.route('/')
def index():
    return render_template("landingPage.html")


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_bp.home'))
            
        else:
            return redirect(url_for('user_bp.login'))
    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))

@user_bp.route('/home')
@login_required
def home():
    return render_template('home.html')



@user_bp.route('/crud')
@login_required
def crud():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    users = User.query.all()
    roles = Role.query.all()
    return render_template('CRUD.html', users=users, roles=roles)

@user_bp.route('/crud/create', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role_name = request.form['role']

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        flash("Role inválida")
        return redirect(url_for('user_bp.crud'))

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return redirect(url_for('user_bp.crud'))

    new_user = User(username=username, email=email, password=password, role=role)
    if new_user.role.name != 'Admin':
            db.session.add(new_user)
            db.session.commit()
            flash("Usuário criado com sucesso")
            return redirect(url_for('user_bp.crud'))
    else:
        flash("Não é permitido criar usuários com a role 'Admin'")
        return redirect(url_for('user_bp.crud'))

@user_bp.route('/crud/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_name = request.form['role']

        other_user = User.query.filter(
            ((User.username == username) | (User.email == email)) & (User.id != user_id)
        ).first()
        if other_user:
            flash("Usuário ou email já existe")
            return redirect(url_for('user_bp.update_user', user_id=user_id))

        user.username = username
        user.email = email
        if password.strip():
            user.password = password
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            flash("Role inválida")
            return redirect(url_for('user_bp.update_user', user_id=user_id))
        user.role = role

        db.session.commit()
        flash("Usuário atualizado com sucesso")
        return redirect(url_for('user_bp.crud'))

    return render_template('update_user.html', user=user, roles=roles)

@user_bp.route('/crud/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Você não pode deletar seu próprio usuário!")
        return redirect(url_for('user_bp.crud'))

    db.session.delete(user)
    db.session.commit()
    flash("Usuário deletado com sucesso")
    return redirect(url_for('user_bp.crud'))
