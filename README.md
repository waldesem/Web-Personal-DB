# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Flask;
- Tornado (as wsgi);
- Sqlite3 (or PostgreSQL);
- Nuxt3 and TailwindCSS;

### Installation

To use this project, you will need to have Python 3.10 or higher.
For installiing the required Python packages run commands:
```
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/server_flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database

SQLite3 Database will be used by default and crated automatically in the first run.
To Use a PostgreSQL Database in Application install PostgreSQL
```
sudo apt-get -y install postgresql postgresql-contrib
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

### Settings

For creating new user run the command in terminal:
```
export FLASK_APP=app
flask user 'Super Admin' super email@example.com --role=admin --region=main
```
For creating default folders destination run the command in terminal:
```
flask folder # optional add 'path/to/folder'
```

### Build frontend

Change directory to web_nuxt and run the command to install packages:
```
npm i
```
To build Nuxt3 with Client-side Only Rendering:
In nuxt.config.ts toggle `ssr: false` and then run the command:
```
npx nuxi generate
```
To build Nuxt3 with Server-side Rendering:
In nuxt.config.ts toggle `ssr: false` and comment `output - publicDir`
Then run the command:
```
npx nuxi build
```
Builded files can be found in `server_flask/app/static`.


Also you can change DATABASE_URI and base_path in config.py and settings.ini

### Start backend

To start a server run the command in terminal:
```
python server.py # for desktop mode; more options see in the server.py
```
To start a frontend server run the command in terminal:
```
HOST=127.0.0.1 PORT=8000 node .output/server/index.mjs
```
DEFAULT_PASSWORD for created user - `88888888`.

### License

This project is licensed under the MIT License.
