from flask import Blueprint, render_template, request, redirect, url_for, after_this_request, flash
from flask import session

from testFlask import db
from flask_login import login_required, current_user
from testFlask.models import User, AlchemyEncoder, Place, Room
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('floor1.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/floor1')
# @login_required
def floor1():
    return render_template('floor1.html')

@main.route('/floor3')
# @login_required
def floor3():
    return render_template('floor3.html')

@main.route('/room/<room_name>')
def show_room(room_name):
    if room_name[-1] == 'А':
        return redirect('/antresol/' + room_name[:-1])
    return render_template('room.html', name=room_name, number=session.get('number', None),
                           text=session.get('text', None), type=session.get('type', None), floor=room_name[0])


#
# @main.route('/room/x')
# def show_room(room_name, place):
#     return render_template('room.html', name=room_name, place=place)


@main.route('/antresol/<antresol_name>')
def show_antresol(antresol_name):
    return render_template('antresol.html', name=antresol_name, number=session.get('number', None),
                           text=session.get('text', None), type=session.get('type', None), floor=antresol_name[0])


@main.route('/navigation')
def navigate():
    return render_template('navigation.html')


@main.route('/navigation', methods=['POST'])
def find_path():
    c_from = request.form.get('from')
    c_to = request.form.get('to')

    room_from = Room.query.filter_by(name=c_from).first()
    if room_from is None:
        flash('Начальной комнаты не существует')
        return redirect(url_for('main.navigate'))
    room_to = Room.query.filter_by(name=c_to).first()
    if room_to is None:
        flash('Конечной комнаты не существует')
        return redirect(url_for('main.navigate'))

    flash('Простите, не получилось построить маршрут')
    return redirect(url_for('main.navigate'))


# @main.route('/room/<room_name>/<number>')
# def show_user(room_name, number):
#     users = User.query.filter_by(room_id)
@main.route('/room/<room_name>/<number>')
def show_user_room(room_name, number):
    # users = User.query.filter_by(room_id)
    session['number'] = number

    room = Room.query.filter_by(name=room_name).first()
    place = Place.query.join(Room, Place.room_id == Room.id) \
        .filter(Place.number == number).filter(Room.name == room_name).first()
    users = None
    text = []
    if place is not None:
        users = place.users
        for user in users:
            text += [user.name + " " + user.surname + " " + user.email]
        if not text:
            text = ['Пустое место']
        session['text'] = text
        session['type'] = room.type
        return redirect('/room/' + room_name + '#place' + number)
    return redirect('/room/{}'.format(room_name))


@main.route('/antresol/<antresol_name>/<number>')
def show_user_antresol(antresol_name, number):
    # users = User.query.filter_by(room_id)
    session['number'] = number

    room = Room.query.filter_by(name=antresol_name).first()
    place = Place.query.join(Room, Place.room_id == Room.id) \
        .filter(Place.number == number).filter(Room.name == antresol_name + 'А').first()
    text = []
    if place is not None:
        users = place.users
        for user in users:
            text += [user.name + " " + user.surname + " " + user.email]
        if not text:
            text = ['Пустое место']
        session['text'] = text
        session['type'] = room.type
        return redirect('/antresol/' + antresol_name + '#place' + number)
    return redirect('/antresol/{}'.format(antresol_name))


def get(room_name, text_stair):
    room = Room.query.filter_by(name=room_name).first()
    if room is not None:
        places = Place.query.filter_by(room_id=room.id).all()
        text = []
        for place in places:
            users = place.users
            for user in users:
                text += [user.name + " " + user.surname + " " + user.email]
        if not text and room_name != '113-114' and room_name != '132-133'\
                and room_name != '309-310' and room_name != '323-324':
            text = ['Пустая комната']
        name_ = 'Комната ' + room_name + ' ' + room.type
    else:
        name_ = 'Проиграл'
        if room_name.startswith('lyft'):
            name_ = 'Лифт'
        elif room_name.startswith('stairs'):
            name_ = 'Лестница'
        text = [text_stair]
    return room_name, name_, text


@main.route('/floor1/<room_name>')
def show_floor1_room_notif(room_name):
    if '.' in room_name:
        room_name2, name_2, text2 = get(room_name.split('.')[1], 'подняться')
        room_name, name_, text = get(room_name.split('.')[0], 'подняться')
        return render_template('floor1_room.html', name=room_name, full_name=name_, text=text,
                               name2=room_name2, full_name2=name_2, text2=text2)
    else:
        room_name, name_, text = get(room_name, 'подняться')
        return render_template('floor1_room.html', name=room_name, full_name=name_, text=text, name2=None)


@main.route('/floor3/<room_name>')
def show_floor3_room_notif(room_name):
    if '.' in room_name:
        room_name2, name_2, text2 = get(room_name.split('.')[1], 'спуститься')
        room_name, name_, text = get(room_name.split('.')[0], 'спуститься')
        return render_template('floor3_room.html', name=room_name, full_name=name_, text=text,
                               name2=room_name2, full_name2=name_2, text2=text2)
    else:
        room_name, name_, text = get(room_name, 'спуститься')
        return render_template('floor3_room.html', name=room_name, full_name=name_, text=text, name2=None)

@main.route("/search")
def search():
    text = "%{}%".format(request.args['searchText'])  # get the text to search for
    # create an array with the elements of BRAZIL_STATES that contains the string
    # the case is ignored

    result = Room.query.filter(Room.name.like(text.lower())).all()[:10]
    if len(result) != 0: return json.dumps({"results": result}, cls=AlchemyEncoder)

    result = Room.query.filter(Room.full_type.like(text.lower())).all()[:10]
    if len(result) != 0: return json.dumps({"results": result}, cls=AlchemyEncoder)

    result = User.query.filter(User.full_name.like(text.lower())).all()[:10]
    if len(result) != 0: return json.dumps({"results": result}, cls=AlchemyEncoder)

    return json.dumps({"results": result}, cls=AlchemyEncoder)
    # result = [User(name="Не найдено", surname="")]
    # result = [c for c in BRAZIL_STATES if text.lower() in c.lower()]
    # return as JSON
