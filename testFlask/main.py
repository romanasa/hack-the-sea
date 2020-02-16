from flask import Blueprint, render_template, request
from testFlask import db
from flask_login import login_required, current_user
from testFlask.models import User, AlchemyEncoder
import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/floor1')
#@login_required
def floor1():
    return render_template('floor1.html')


@main.route('/floor3')
#@login_required
def floor3():
    return render_template('floor3.html')


@main.route('/room/<room_name>')
def show_room(room_name):
    return render_template('room.html', name=room_name)


@main.route('/antresol/<antresol_name>')
def show_antresol(antresol_name):
    return render_template('antresol.html', name=antresol_name)


# @main.route('/room/<room_name>/<number>')
# def show_user(room_name, number):
#     users = User.query.filter_by(room_id)


@main.route("/search")
def search():
    text = "%{}%".format(request.args['searchText'])  # get the text to search for
    # create an array with the elements of BRAZIL_STATES that contains the string
    # the case is ignored
    result = User.query.filter(User.full_name.like(text.lower())).all()[:10]
    if len(result) == 0:
        result = [User(name="Не найдено", surname="")]
    # result = [c for c in BRAZIL_STATES if text.lower() in c.lower()]
    # return as JSON
    return json.dumps({"results": result}, cls=AlchemyEncoder)