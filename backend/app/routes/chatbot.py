from datetime import datetime
import json

from flask import request
from flask_jwt_extended import current_user
from flask.views import MethodView
import redis

from . import bp
from ..routes.login import r_g
from ..models.classes import Groups
from ..analysis.analysis import Matches


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
        
        data_parse = Matches(json_data)
        query = data_parse.get_matches()
        if query:
            response = 'По вашему запросу ничего не найдено. \
                    Попробуйте изменить запрос'
        else:
            response = f'По вашему запросу найдено: {query}'

        self.redis_chat('chatBot', prefix, response)
        return {'chatBot': f'{response}'}
    
    def redis_chat(self, username, prefix, message):
        """
        This function is responsible for managing the chat messages in Redis.
        Parameters:
            username (str): The username of the chat participant.
            prefix (str): The prefix used to identify the chat.
            message (str): The content of the chat message.
        Returns:
            None
        """
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
