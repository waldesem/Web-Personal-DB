# StaffSec

StaffSec is a web interface for managing a candidates database.

### The technology stack used in this project:

- Flask;
- Sqlite;
- Nuxt;

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

For creating settings.ini file run in terminal (Linux, macOS и WSL):

```
chmod +x settings.sh
./settings.sh
```

For creating alphabeth folders in destination directory run (Linux, macOS и WSL):

```
chmod +x folders.sh
./folders.sh
```

For creating new user:

```
source .venv/bin/activate
export FLASK_APP=app
flask command user Super superadmin 'superadmin@localhost.ru' --role=admin
```

Recomend to create user with role `admin` for first login.
DEFAULT_PASSWORD for created user set in settings.ini.

### Build frontend (if needs)

First install Node.js. Then run in terminal:

```
cd Web-Personal-DB/web_nuxt
npm i
```

To build Nuxt with Client-side Rendering:

```
npx nuxi generate
```

Builded files can be found in `server_flask/app/static`.

For Server-Side rendering change SSR=true in env file and execute command:

```
npx nuxt build
```

Builded files can be found in `web_nux/.output`.

### Start backend server

To start server run the command in terminal:

```
uv run server.py # for desktop mode; more options see in the server.py
```

### Start frontend server (if needs)

For starting frontend in SSR mode run

```
HOST=localhost PORT=8000 node .output/server/index.mjs
```

Nitro server should be run behind a reverse proxy like nginx.
