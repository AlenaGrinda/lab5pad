import models
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "312"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return models.User.get_user_by_id(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template(
            'index.html',
            lab_name="Лабораторная работа 5",
            lab_description="Страница index лабораторной работы 5",
            logout_url=url_for('logout'),
        )
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Неправильный email или пароль, или такого пользователя не существует", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = models.User.get_user_by_email(email)
        if existing_user:
            flash("Пользователь с таким email уже существует", "error")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        if models.User.create_user(name, email, hashed_password):
            flash("Регистрация успешна! Теперь вы можете войти", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка регистрации. Попробуйте снова", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))