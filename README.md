# StaffSec

StaffSec is a web interface for managing a candidates database.

### The technology stack used in this project:

- Litestar;
- PostreSQL;
- Nuxt;

### Installation

To use this project, you will need to have Python 3.14 version.
For installiing the required Python packages run commands:

```
wget -qO- https://astral.sh/uv/install.sh | sh
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/server_litestar
uv sync
source .venv/bin/activate
```

#### Build rust module for validating inn and snils (Optional):

You needs instal rust language and maturin package.

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pipx install maturin
cd rust
maturin build --release --interpreter $(which python)
uv pip install target/wheels/checksum-0.1.0-cp314-cp314-manylinux_2_34_x86_64.whl
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

Create in server_litestar folder `.env` file with content:

```
BASE_PATH=/home/MyProjects/Web-Personal-DB/server_litestar/PersonalDB

DEFAULT_PASSWORD=88888888

PG_HOST=localhost
PG_PORT=5433
PG_DATABASE=personal
PG_USER=webapp
PG_PASSWORD=webapp
```

### Build frontend

First install latest stable NodeJS version.
Then run in terminal:

```
cd Web-Personal-DB/web_nuxt
npm i
npx nuxi generate
```

Builded files can be found in `server_litestar\app\static`

### Start backend server

To start server run the command in terminal:

```
litestar run --reload
```

or for production:

```
uvicorn app:app # for uvicorn ASGI server
granian --interface asgi app:app # for Granian Rust-based ASGI server
```
