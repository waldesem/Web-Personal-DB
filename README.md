# Web-Personal-DB

Web-Personal-DB is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python (Flask, APIFlask, SQLAlchemy, Marshmallow)
- TypeScript
- JavaScript
- Bootstrap 5 (journal theme)

### Installation
To use this project, you will need to have Python 3.7 or higher installed on your local machine. You can follow the instructions here to install Python if you don't have it already.

Once you have Python installed, you can install the required Python packages by running the following command in your terminal:
```
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
GRANT ALL PRIVILEGES ON DATABASE personal TO sammy;
\q
```

### Usage
For create database enter command in flask shell:
```
flask shell
db.create_all()
```

For create admin user enter command in flask shell:
```
from app import db, User
admin = User(fullname='fullname', username='username', password='password')
role = Role(name='admin')
roles_users = (user_id=1, role_id=1)
db.session.add(admin)
db.session.add(role)
db.session.add(roles_users)
db.session.commit()
```

To start the web application, run the following command in your terminal:
```
export FLASK_APP=app
export FLASK_DEBUG=1        # for debug mode
flask run
```

This will start the Flask server and serve the application at http://localhost:5000/.

For migrate database enter commands:
```
flask db init       # only first time if migration folder is not exist
flask db migrate
flask db upgrade
```

You will also need to have Node.js installed on your machine to build and run the TypeScript code.
After installing Node.js, you can install the required npm packages by running the following command in your terminal:
```
npm install -g typescript
```
To build the TypeScript code, run the following command in your terminal:
```
npm run build
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory.

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