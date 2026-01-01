# StaffSec

StaffSec is a web interface for managing a candidates database.

### The technology stack used in this project:

- Flask;
- PostreSQL;
- Nuxt;

### Installation

To use this project, you will need to have Python 3.12 or higher.
For installiing the required Python packages run commands:

```
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/server_flask
wget -qO- https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv sync
```

### Database

PostreSQL must be installed before the first run.

```
sudo ufw allow 5433/tcp
sudo apt install postgresql postgresql-contrib -y
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Configuring Remote Access

```
sudo nano /etc/postgresql/16/main/postgresql.conf
```

Change `listen_addresses = '*'`

Create user and database:

```
sudo -i -u postgres
psql
CREATE DATABASE personal;
CREATE USER webapp WITH PASSWORD 'webapp';
GRANT ALL PRIVILEGES ON DATABASE personal TO webapp;
\c personal
GRANT USAGE ON SCHEMA public TO webapp;
GRANT CREATE ON SCHEMA public TO webapp;
GRANT ALL ON ALL TABLES IN SCHEMA public TO webapp;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO webapp;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO webapp;

\q
exit
```

### Settings

For creating .env file run in terminal (Linux, macOS и WSL):

```
chmod +x dotenv.sh
./dotenv.sh
```

CHANGE DESTIONATION FOR `BASE_PATH` AS YOU NEED

For creating alphabeth folders in destination directory run (Linux, macOS и WSL):

```
chmod +x folders.sh
./folders.sh
```

For creating new user:

```
export FLASK_APP=app
flask command user Super superadmin 'superadmin@localhost.ru' --role=admin
```

Recomend to create user with role `admin` for first login.
DEFAULT_PASSWORD for created user set in dotenv.sh.

### Build frontend

First install Node.js. Then run in terminal:

```
cd Web-Personal-DB/web_nuxt
npm i
```

For Server-Side rendering change SSR=true in env file and execute command:

```
npx nuxt build
```

Builded files can be found in `web_nux/.output`.

### Start backend server

To start server run the command in terminal:

```
uv run flask run --port=8000 --host=127.0.0.1 --debug
```

or for production:

```
gunicorn wsgi:app # for prod mode
```

### Start frontend server (if Server-Side rendering enabled)

For starting frontend in SSR mode run

```
HOST=localhost PORT=8000 node .output/server/index.mjs
```

Nitro server should be run behind a reverse proxy like nginx.

Use `npx npm-check-updates -u` for update packages for latest versions.

### Use Docker

For building image run:

```
docker compose up --build -d
```

Run container:

```
docker run -d -p 8000:8000 --name flask-app my-flask-app
```

Manage container:

```
docker compose ps

docker compose logs -f

docker compose down

docker compose down --rmi all
```
