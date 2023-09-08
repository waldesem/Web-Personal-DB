# StaffSec

StaffSec is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python3;
- APIFlask a lightweight Python web API framework based on Flask and marshmallow-code projects;
- Gunicorn as HTTP server;
- Flask-JWT-Extended as a tool for authorization;
- Flask-SQLAlchemy as tool that adds support for SQLAlchemy;
- Flask-Marshmallow as integration layer for Flask and marshmallow (an object serialization/deserialization library);
- Flask-Migrate as a tool that handles SQLAlchemy database migrations using Alembic;
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
sudo apt install python3 python3-pip python3-venv
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
sudo systemctl enable postgresql.service
```
Creating the PostgreSQL Database and User
```
sudo -iu postgres psql
CREATE DATABASE personal;
CREATE USER flask WITH PASSWORD 'flask';
GRANT ALL PRIVILEGES ON DATABASE personal TO flask;
\q
```

### Migration

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
To start development node server  run the following command in your terminal:
```
npm run dev
```
To build the code in the static directory flask app, first comment/uncomment rows in server.ts. 
Then, run the following command in your terminal:
```
npm run build
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

### Usage

To start the application at http://localhost:5000 run the following command in your terminal:
```
export FLASK_APP=app
export FLASK_ENV=testing  # create a testing environment and SQLite database (optional)
flask run
```
Database tables creates automatically. Admin user on default has name admin and the password 'administrator'.
Change it in first login to application. Regions gets from the classify file
Then you can start the app with Gunicorn server:
```
gunicorn -c gunicorn.conf.py wsgi:app  # start the gunicorn server with the settings in gunicorn.conf.py
```

### Gunicorn Service

For create systemd service run the following command in your terminal:
```
sudo nano /etc/systemd/system/staffsec.service
```
Add the following line:
```
[Unit]
Description=Gunicorn instance to serve staffsec
After=network.target
[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/DB-Personal-DB/backend
Environment="PATH=/home/user/DB-Personal-DB/backend/venv/bin"
ExecStart=/home/user/DB-Personal-DB/backend/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
[Install]
WantedBy=multi-user.target
```
Start the service:
```
sudo systemctl start staffsec
sudo systemctl enable staffsec
sudo systemctl status staffsec
```

### Nginx

Nginx configuration:
Open the file '/etc/nginx/sites-available/staffsec' and add the following line:
```
server {
    listen 80;
    server_name yourdomain.com;
    location / {
        include proxy_params;
        proxy_pass http://0.0.0.0:5000;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
Add configuration file '/etc/nginx/sites-enabled/staffsec' and restart Nginx:
```
sudo ln -s /etc/nginx/sites-available/staffsec /etc/nginx/sites-enabled/staffsec
sudo service nginx restart
```
Add rule in your firewall:
```
sudo ufw allow 'Nginx HTTP'
sudo ufw reload
```

### License
This project is licensed under the MIT License. See the LICENSE file for details.