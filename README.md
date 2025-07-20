# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Flask;
- Tornado (as wsgi);
- Sqlite3;
- Nuxt3 and NuxtUI with TailwindCSS;

### Installation

To use this project, you will need to have Python 3.12 or higher.
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

### Settings

For creating alphabeth folders in destination directory add path in settings.ini.
Then run the command:
```
export FLASK_APP=app # for Windows - $env:FLASK_APP = "app"
flask command folders
```
For creating new user run the command in terminal:
```
export FLASK_APP=app
flask command user 'Super Admin' superadmin superadmin@elocalhost --role=admin
```
Recomend to create user with role `admin` for first login.
DEFAULT_PASSWORD for created user - `88888888`.

### Build frontend

First you need install Bun - an all-in-one toolkit for JavaScript and TypeScript apps.
Change directory to web_nuxt and run the command to install packages:
```
bun i
```
To build Nuxt3 with Client-side Only Rendering:
```
bunx nuxi generate
```
Builded files can be found in `server_flask/app/static`.


### Start backend

To start a server run the command in terminal:
```
python server.py # for desktop mode; more options see in the server.py
```
