# StaffSec (in development now, may be broken)

StaffSec is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python3;
- APIFlask a Python web API framework based on Flask and marshmallow-code projects;
- Postgesql as database;
- SQLAlchemy as ORM;
- Redis as caching service;
- Vue3 as the frontend and Vite as Frontend Tooling
- Bootstrap 5 as the UI library.

_For experimental implementation of backend on Golang see [GO-Personal-DB](https://github.com/waldesem/GO-Personal-DB)_

### Installation

To use this project, you will need to have Python 3.10 or higher installed on your local machine.
Check your Python version with the following command:

```
python3 --version
```

For installiing the required Python packages run the following command in the terminal:

```
sudo apt install python3 python3-pip python3-venv # if not install venv yet
git clone https://github.com/waldesem/Web-Personal-DB.git
cd backend
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

### Usage

To start the application at http://localhost:5000 run the following command in your terminal:

```
flask create       # create default tables and populate them with data from the classes.py file
gunicorn -c gunicorn.conf.py wsgi:app  # start the gunicorn server with the settings in gunicorn.conf.py
```

Admin user on default has name 'admin'.
Default password for all app users is `88888888`
Change it in first login to application.

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
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;
    }
    location /samba {
        proxy_pass http://0.0.0.0:445;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;
    }
}
```

Add configuration file '/etc/nginx/sites-enabled/staffsec' and restart Nginx:

```
sudo ln -s /etc/nginx/sites-available/staffsec /etc/nginx/sites-enabled/staffsec
# sudo ln -sf /etc/nginx/sites-available/staffsec /etc/nginx/sites-enabled/staffsec # for upgrade
sudo service nginx restart
```

Add rule in your firewall:

```
sudo ufw allow 'Nginx HTTP'
sudo ufw reload
```

### Node Development (optional)

You will also need to have Node.js installed on your machine to build and run the TypeScript code.
After installing Node.js, you can install the required npm packages by running in your webapp directory the following command in your terminal:

```
npm i
```

To start development node server run the following command in your terminal:

```
npm run dev
```

To build the code in the static directory flask app, first comment/uncomment the lines `server` in /Web-Personal-DB/frontend/src/utilities/utils.ts
Then run the following command in your terminal:

```
npm run build
```

This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

### License

This project is licensed under the MIT License.

### Screenshots

![Screenshot](https://github.com/waldesem/Web-Personal-DB/blob/stable/screenshots/1.png?raw=true)
![Screenshot](https://github.com/waldesem/Web-Personal-DB/blob/stable/screenshots/2.png?raw=true)
![Screenshot](https://github.com/waldesem/Web-Personal-DB/blob/stable/screenshots/3.png?raw=true)
![Screenshot](https://github.com/waldesem/Web-Personal-DB/blob/stable/screenshots/4.png?raw=true)
