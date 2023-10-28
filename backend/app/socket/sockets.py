from flask_socketio import emit

from .. import socketio
# from ..routes.login import r_g
# from ..models.classes import Groups


@socketio.on('connect')
def connect():
    emit('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

# @r_g.group_required(Groups.staffsec.name)
@socketio.on('incoming')
def handle_incoming_event(message):
    print(message)

#@r_g.group_required(Groups.staffsec.name)
@socketio.on('outcoming')
def handle_outcoming_event(json):
    emit('income', json)

@socketio.on_error_default 
def default_error_handler(e):
    emit('error', e)
