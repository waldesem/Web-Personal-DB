# StaffSec

StaffSec is a web interface for managing a candidate database. It includes a database model and an API for submitting/retrieving candidate applications and the results of automatic verification.

### The main technology stack used in this project includes:

- Python3;
- APIFlask;
- Postgesql;
- SQLAlchemy;
- Redis;
- Vue3;
- Bootstrap 5.

### Installation

To use this project, you will need to have Python 3.10 or higher installed on your local machine.
For installiing the required Python packages run the following command in the terminal:

```
sudo apt install python3 python3-pip python3-venv # if not install venv yet
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To Use a PostgreSQL Database in Application install PostgreSQL

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

### Start backend

To create application run the following command in your terminal:
```
flask init         # init environments
```
In .env file change SQLALCHEMY_DATABASE_URI to your PostgreSQL credentials then run the command.
```
flask create       # create default values
```
To start the application at http://localhost:5000 run the following command in your terminal:
```
flask run          # start the application
waitress-serve --host 127.0.0.1 --port 5000 --threads=8 wsgi:app  # start the waitress server
```

Default user for application has name 'superadmin'.
DEFAULT_PASSWORD for all app users is `88888888`. You can change it in config.py file.
Change it in first login to application.

### Frontend build

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

### WSGI Service

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
ExecStart=/home/user/DB-Personal-DB/backend/venv/bin/waitress -c waitress-serve --host 127.0.0.1 --port 5000 wsgi:app
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
        proxy_pass http://127.0.0.1:5000;
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

### License

This project is licensed under the MIT License.
