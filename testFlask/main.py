from flask import Blueprint, render_template
from testFlask import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/floor3')
#@login_required
def floor3():
    return render_template('floor3.html')