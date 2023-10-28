from flask_socketio import emit

from .. import socketio
from ..routes.login import r_g
from ..models.classes import Groups


@r_g.group_required(Groups.staffsec.name)
@socketio.on('connect')
def connect():
    emit('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@r_g.group_required(Groups.staffsec.name)
@socketio.on('income')
def handle_income_event(json):
    print('received json: ' + str(json))

@r_g.group_required(Groups.staffsec.name)
@socketio.on('outcome')
def handle_outcome_event(json):
    emit('income', json)

@socketio.on_error_default 
def default_error_handler(e):
    emit('error', e)
