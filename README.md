# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Flask;
- Sqlite;
- Nuxt4;

### Installation

To use this project, you will need to have Python 3.12 or higher.
For installiing the required Python packages run commands:
```
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/server_flask
wget -qO- https://astral.sh/uv/install.sh | sh
uv venv
uv sync
```

### Database

SQLite3 Database will be used by default and crated automatically in the first run.

### Settings

For creating alphabeth folders in destination directory add path in settings.ini.
Then run the command:
```
export FLASK_APP=app
flask command folders
```
For creating new user run the command in terminal:
```
flask command user Super superadmin 'superadmin@localhost.ru' --role=admin
```
Recomend to create user with role `admin` for first login.
DEFAULT_PASSWORD for created user - `88888888`.

### Build frontend

First you need install Node.js a JavaScript runtime environment. Then:
```
cd Web-Personal-DB/web_nuxt
npm i
```
To build Nuxt4 with Client-side Only Rendering:
```
npx nuxi generate
```
Builded files can be found in `server_flask/app/static`.

### Start backend

To start a server run the command in terminal:
```
uv run server.py # for desktop mode; more options see in the server.py
```
