# StaffSec

StaffSec is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python;
- Flask (APIFlask) as the web server;
- Flask-JWT-Extended for authorization;,
- Flask-SQLAlchemy (SQLAlchemy) as ORM and database;
- Flask-Marshmallow (Marshmallow) as validation and serialization of data;
- Vue3 as the frontend and Vite as Frontend Tooling
- Bootstrap 5 as the UI framework.

### Installation
To use this project, you will need to have Python 3.10 or higher installed on your local machine. You must install Python if you don't have it already.
Check your Python version with the following command:
```
python3 --version
```

Once you have Python installed, you can install the required Python packages by running the following command in your terminal:
```
sudo apt install python3-pip
sudo apt install python3-venv
mkdir staffsec
cd staffsec
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To Use a PostgreSQL Database in a Flask Application install PostgreSQL (Ubuntu example)
```
sudo apt-get -y install postgresql
sudo systemctl start postgresql.service
```
Creating the PostgreSQL Database and User
```
sudo -iu postgres psql
CREATE DATABASE personal;
CREATE USER flask WITH PASSWORD 'flask';
GRANT ALL PRIVILEGES ON DATABASE personal TO flask;
\q
```

### Usage

To start the application at http://localhost:5000 run the following command in your terminal:
```
export FLASK_APP=app
export FLASK_ENV=testing  # create a testing environment and SQLite database (optional)
flask run
```
If you need to run the server with specific host and port:
```
flask run --host=0.0.0.0 --port=5000
```
Start the app with Gunicorn server:
```
gunicorn -c gunicorn.conf.py wsgi:app
```
Database tables creates automatically. Admin user on default has name admin and the same password.
You must change it in first login to application

For migrate database enter commands:
```
flask db init       # run this command for the first time if migration folder is not exist
flask db migrate    # after change db schema
flask db upgrade    # after change db schema
```

### Node Development (optional)
You will also need to have Node.js installed on your machine to build and run the TypeScript code.
After installing Node.js, you can install the required npm packages by running in your webapp directory the following command in your terminal:
```
npm i
```
To start development node server, run the following command in your terminal:
```
npm run dev
```
To build the code in the static directory flask app, first comment/uncomment rows in server.ts. 
Then, run the following command in your terminal:
```
npm run build
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

### License
This project is licensed under the MIT License. See the LICENSE file for details.