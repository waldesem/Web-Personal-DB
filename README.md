# StaffSec

StaffSec is a web interface for managing a candidates database.

## The technology stack used in this project

- Litestar is a powerful, lightweight and flexible ASGI framework;
- Piccolo is a modern, async query builder and ORM;
- PostreSQL is a powerful, open source object-relational database system;
- Nuxt is a free and open-source framework with Vue.js;

## Installation (Linux)

To use this project, you will need to have Python 3.14 version.
For installiing the required Python packages run commands:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/server_litestar_piccolo
uv sync
source .venv/bin/activate
```

### Build Rust module for validating inn and snils (Optional)

```bash
uv tool install maturin
cd rust
maturin develop
```

### Database

PostreSQL must be installed before the first run.

```bash
sudo ufw allow 5433/tcp
sudo apt install postgresql postgresql-contrib -y
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Configuring Remote Access

```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

Change `listen_addresses = '*'`

Create user and database:

```bash
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

Create in server_litestar_piccolo folder `.env` file with content:

```bash
BASE_PATH=/home/user/PersonalDB

DEFAULT_PASSWORD=88888888

PG_HOST=localhost
PG_PORT=5433
PG_DATABASE=personal
PG_USER=webapp
PG_PASSWORD=webapp
```

### Build frontend (Optional)

First install latest stable NodeJS version.
Then run in terminal:

```bash
cd Web-Personal-DB/web_nuxt
npm i
npx nuxi generate
```

Builded files can be found in `server_litestar_piccolo\app\static`

### Start backend server

To start server run the command in terminal:

```bash
litestar run --reload
```

or for production:

```bash
uvicorn app:app # for uvicorn ASGI server

granian --interface asgi app:app # Rust-based ASGI server (needs to install: uv add granian)
```
