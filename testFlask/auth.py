from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from testFlask import db
from testFlask.models import User, Room, Place
from flask_login import login_user, login_required, logout_user, current_user
#hello
auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if password != confirm:
        flash('Passwords must be equal')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), surname=None,
                    name=None, place=None)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Invalid email or password')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    if user.surname is None or user.name is None:
        flash('Пожалуйста, заполните информацию')
        return redirect(url_for('auth.settings'))

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@auth.route('/settings', methods=['POST'])
@login_required
def settings_post():
    room_num = request.form.get('room_num')
    place_num = request.form.get('place_num')

    room = Room.query.filter_by(name=room_num).first()
    if room is None:
        flash('Комнаты не существует')
        return redirect(url_for('auth.settings'))

    place = Place.query.join(Room, Place.room_id == Room.id) \
        .filter(Place.number == place_num).filter(Room.name == room_num).first()

    if place is None:
        flash('Места не существует')
        return redirect(url_for('auth.settings'))

    if current_user.name is None:
        current_user.name = request.form.get('name')
    if current_user.surname is None:
        current_user.surname = request.form.get('surname')

    current_user.place = place
    return redirect(url_for('main.index'))