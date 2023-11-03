from datetime import datetime
import json

from flask import request
from flask_jwt_extended import current_user
from flask.views import MethodView
import redis

from . import bp
from ..routes.login import r_g
from ..models.classes import Groups
from ..analysis.analysis import parse_data


redis_chat = redis.StrictRedis(
    host="localhost", port=6379, db=1, decode_responses=True
)
    
class ChatView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def post(self):
        json_data = request.get_json()
        username = current_user.username
        prefix = f'{username}_chat'
        message = json_data['data']
        self.redis_chat(username, prefix, message)
        
        query = parse_data(json_data)
        if query[0] == 'error':
            return {
                'chatBot': 'По вашему запросу ничего не найдено. \
                    Попробуйте изменить запрос'
                }
        else:
            match query[0]:
                case 'anketa':
                    response = f'По вашему запросу найдено: {(", ").join(query[1])}. \
                        Показано {len(query[1])} результатов из {query[2]}'

                    self.redis_chat('chatBot', prefix, response)
                    return {'chatBot': f'{response}'}
    
    def redis_chat(self, username, prefix, message):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not redis_chat.hget(prefix, username):
            redis_chat.hset(prefix, username, json.dumps(
                [{
                    'message': message,
                    'time': time
                }]
            ))
        else:
            redis_chat.rpush('f{prefix:username}', json.dumps(
                {
                    'message': message,
                    'time': time
                }
            ))

bp.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
