import os
import shutil

from flask import request, current_app, send_file
from flask.views import MethodView

from . import bp
from .login import roles_required, group_required
from ..models.classes import Roles, Groups

class FileManagementView(MethodView):

    decorators = [group_required(Groups.staffsec.name),
                  roles_required(Roles.user.name), 
                  bp.doc(hide=True)]
    
    def __init__(self):
        self.dirs = []
        self.files = []
        self.current_path = [] # 'Home'
        self.base_path = current_app.config["BASE_PATH"] + '/'
    
    async def get(self):
        """
        Retrieves the list of directories and files in the current path.
        Returns:
            dict: A dictionary containing the current path, list of directories, and list of files.
                - 'path' (str): The current path.
                - 'dirs' (list): A list of directories in the current path.
                - 'files' (list): A list of files in the current path.
        """
        path = os.path.join(self.base_path, *self.current_path)
        items = os.listdir(path)
        self.dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        self.files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        print(self.current_path, self.dirs, self.files)
        return {'path': self.current_path, 
                'dirs': self.dirs, 
                'files': self.files}

    def post(self, action):
        """
        Handles different actions for the POST request.
        Parameters:
        - action (str): The action to be performed.
        Returns:
        - The result of the action.
        """
        json_data = request.get_json()
        self.current_path = json_data['path']
        match action:
            case 'open':
                new_path = os.path.join(self.base_path, *self.current_path, json_data['item'])
                if os.path.isdir(new_path):
                    self.current_path.append(json_data['item'])
                    return self.get()
                
            case 'parent':
                new_path = os.path.join(self.base_path, *self.current_path)
                if os.path.isdir(new_path):
                    return self.get()

            case 'download':
                new_path = os.path.join(self.base_path, *self.current_path, json_data['item'])
                if os.path.isfile(new_path):
                    return send_file(new_path, as_attachment=True)
            
            case 'create':
                new_path = os.path.join(self.base_path, *self.current_path, 'Новая папка')
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                return self.get()
            
            case 'rename':
                new_path = os.path.join(self.base_path, *self.current_path, json_data['new'])
                if not os.path.isdir(new_path):
                    os.rename(os.path.join(self.base_path, *self.current_path, json_data['old']),
                            os.path.join(new_path))
                    return self.get()
           
            case 'copy':
                for item in json_data['new']:
                    source = os.path.join(self.base_path, *json_data['old'], item)
                    destination = os.path.join(self.base_path, *self.current_path, item)

                    if os.path.isdir(source):
                        shutil.copytree(source, destination)
                    else:
                        shutil.copy(source, destination)
                return self.get()
            
            case 'сut':
                for item in json_data['new']:
                    shutil.move(os.path.join(self.base_path, *json_data['old'], item),
                                os.path.join(self.base_path, *self.current_path, item))
                return self.get()

            case 'delete':
                items_paths = [os.path.join(self.base_path, *self.current_path, item) \
                               for item in json_data['items']] 
                for item_path in items_paths:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                return self.get()
            

files_view = FileManagementView.as_view('manager')
bp.add_url_rule('/manager', view_func=files_view, methods=['GET'])
bp.add_url_rule('/manager/<action>', view_func=files_view, methods=['POST', 'PATCH'])
