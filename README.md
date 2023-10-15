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
To build the code in the static directory flask app, run the following command in your terminal:
```
npm run build
```
This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

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
flask run
```
Admin user on default has name 'admin'.
Default password for all app users is `88888888`
Change it in first login to application.

To start the app with Gunicorn server:
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
sudo service nginx restart  # or sudo service nginx reload
```
Add rule in your firewall:
```
sudo ufw allow 'Nginx HTTP'
sudo ufw reload
```

### Samba Configuration for Opening Files on Windows from Ubuntu Server (not tested yet)

Install Samba on your Linux server if it is not already installed.
```
sudo apt install samba
```
Open the Samba configuration file using a text editor:
```
sudo nano /etc/samba/smb.conf
```
In the Samba configuration file, add the following lines to the configuration file to define a share:
```
[persons]
path = /root/Web-Personal-DB/persons  # See a BASE_PATH from config.py
writable = yes
guest ok = no
valid users = @smbgroup
create mask = 0664
directory mask = 0775
```
Save the changes to the Samba configuration file and exit the text editor.
Then you must create samba group and account for unix user that will have access to the shared directory.
```
sudo adduser username smbgroup
```
Set a password for the Samba user that will have access to the shared directory. 
You can do this by running the following command, replacing `username` with the desired username:
```
sudo smbpasswd -a username
```
Start the Samba service:
```
sudo systemctl start smbd
sudo systemctl enable smbd
sudo service smbd restart # or sudo service smbd reload
sudo ufw allow Samba
sudo ufw reload
```

On your Windows machine, open File Explorer and enter the IP address or hostname of the Linux server in the address bar, using the following format:
```
\\server_ip_address\persons
```
Replace `server_ip_address` with the actual IP address of your Linux server.
You will be prompted for to enter a username and password for the Samba user that will have access to the shared directory.

### Doker (not tested yet)
To build the docker image run the following command in your terminal:
```
docker build -t staffsec .
docker run --add-host host.docker.internal:host-gateway -p 5000:5000 staffsec
```

### License
This project is licensed under the MIT License.