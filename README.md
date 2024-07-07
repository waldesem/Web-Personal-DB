# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project includes:

- Flask;
- Sqlite3;
- Vue3;
- Bootstrap 5.

### Installation

To use this project, you will need to have Python 3.10 or higher.
For installiing the required Python packages run commands:
```
sudo apt install python3 python3-pip python3-venv # if not install venv yet
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start backend

To create database and admin user run in terminal:
```
python3 create.py
```
To start a server run the command in terminal:
```
python server.py # for debug mode; 
python server.py --actions develop # for development mode 
python server.py --actions prod # for wsgi waitress server
```
Default user for application has name 'superadmin'.
DEFAULT_PASSWORD for all created users - `88888888`.

### License

This project is licensed under the MIT License.
