# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Flask;
- Sqlite3 (or PostgreSQL);
- Vue3 and Bootstrap5 or Nuxt3 and TailwindCSS;

### Installation

To use this project, you will need to have Python 3.10 or higher.
For installiing the required Python packages run commands:
```
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/backend
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

### Build frontend

To build Vue3 frontend run the command in terminal:
```
cd frontend
npm i
npm run build
```
To build Nuxt3 (in development) with Client-side Only Rendering run the command:
```
cd webapp
npm i
npx nuxi generate
```
Builded files can be found in `backend/app/static`.

### Settings

Change DATABASE_URI and base_path in config.py and settings.ini

### Start application

To start a server run the command in terminal:
```
python server.py # for desktop mode; more options see in the server.py
```
Default admin user for application has name `superadmin`.
DEFAULT_PASSWORD for created user - `88888888`.

### License

This project is licensed under the MIT License.
