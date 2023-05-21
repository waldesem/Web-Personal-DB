# Web-Personal-DB

Web-Personal-DB is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

Python (Flask, APIFlask, SQLAlchemy, Marshmallow, WTForms)
- TypeScript
- JavaScript
- Bootstrap 5

### Installation
To use this project, you will need to have Python 3.7 or higher installed on your local machine. You can follow the instructions here to install Python if you don't have it already.

Once you have Python installed, you can install the required Python packages by running the following command in your terminal:
```
pip install -r requirements.txt
```

You will also need to have Node.js installed on your machine to build and run the TypeScript code.

After installing Node.js, you can install the required npm packages by running the following command in your terminal:
npm install

### Usage
To start the web application, run the following command in your terminal:
```
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

This will start the Flask server and serve the application at http://localhost:5000/.

For create database enter command in flask shell:
```
db.create_all()
```

For migrate database enter commands in flask shell:
```
flask db init - only first time if migration folder is not exist
flask db migrate
flask db upgrade
```

To build the TypeScript code, run the following command in your terminal:
```
npm run build
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory.

### Contributing
If you would like to contribute to this project, please follow these steps:

Основной стек технологий: Python (Flask, APIFlask, SQLAlchemy, Marshmallow, WTForms), JavaScript, Bootstrap5

### License
This project is licensed under the MIT License. See the LICENSE file for details.