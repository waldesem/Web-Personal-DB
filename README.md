# StaffSec

StaffSec is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python;
- Flask (APIFlask) as the web server;
- Flask-JWT-Extended for authorization;,
- Flask-SQLAlchemy (SQLAlchemy) as ORM and database;
- Flask-Marshmallow (Marshmallow) as validation and serialization of data;
- Vue3 as the frontend;
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
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To Use a PostgreSQL Database in a Flask Application install PostgreSQL (Ubuntu example)
```
sudo apt install postgresql postgresql-contrib
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

To start the application in test mode, run the following command in your terminal:
```
export FLASK_APP=app
export FLASK_ENV=testing
flask run
```
This will start the Flask server and serve the application at http://localhost:5000/.

If you need to run the server with specific host and port:
```
flask run --host=0.0.0.0 --port=5000
```
Start the app with Gunicorn:
```
gunicorn -b 0.0.0.0:5000 app:app
```
SQLite database and admin user creates automatically with name = admin and password=admin.
You must change it in first login to application

For migrate database enter commands:
```
flask db init       # only first time if migration folder is not exist
flask db migrate
flask db upgrade
```

### Node
You will also need to have Node.js installed on your machine to build and run the TypeScript code.
After installing Node.js, you can install the required npm packages by running in your webapp directory the following command in your terminal:
```
npm i
```
To start development node server, run the following command in your terminal:
```
npm run dev
```
To build the TypeScript code in the static directory, run the following command in your terminal:
```
npm run build -- --dest ../server/app/static
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory.

### Docker (not tested yet)
To build the Docker image, open a terminal or command prompt in the directory containing the Dockerfile and run the following command:
```
docker build -t staff_security_api .
docker run -p 5000:5000 staff_security_api
```
or for testing configuration run the following command:
```
docker build -t staff_security_api_testing --build-arg FLASK_ENV=testing .
docker run -p 5000:5000 -e FLASK_ENV=testing staff_security_api_testing
```

### Contributing
If you would like to contribute to this project, please follow these steps:

- Fork the repo
- Create a new branch (git checkout -b feature/your-feature-name)
- Make your changes
- Commit your changes (git commit -am 'Add some feature')
- Push to the branch (git push origin feature/your-feature-name)
- Create a new Pull Request

### License
This project is licensed under the MIT License. See the LICENSE file for details.