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
Also you must select SQLite3 or PostgreSQL in the config.py


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

<details>
<summary> Upload Sqlite dump to PostgreSQL </summary>
<br>
For upload sqlite dump to PostgreSQL first replace in `/database.db.sql`:
- id INTEGER PRIMARY KEY on SERIAL;
- DATETIME on TIMESTAMP;
- BOOLEAN on INTEGER;

Then run the command:
```
GRANT ALL PRIVILEGES ON SCHEMA public TO flask; # if needed
ALTER DATABASE personal OWNER TO flask; # if needed
psql -U flask -W personal -h localhost -p 5433 < /database.db.sql
```
Convert INTEGER to BOOLEAN:
```
BEGIN;
ALTER TABLE users
  ALTER COLUMN change_pswd DROP DEFAULT,
  ALTER COLUMN blocked DROP DEFAULT,
  ALTER COLUMN deleted DROP DEFAULT;

ALTER TABLE users
  ALTER COLUMN change_pswd TYPE bool USING CASE WHEN change_pswd=0 THEN FALSE ELSE TRUE END,
  ALTER COLUMN blocked TYPE bool USING CASE WHEN blocked=0 THEN FALSE ELSE TRUE END,
  ALTER COLUMN deleted TYPE bool USING CASE WHEN deleted=0 THEN FALSE ELSE TRUE END;

ALTER TABLE users
  ALTER COLUMN change_pswd SET DEFAULT FALSE,
  ALTER COLUMN blocked SET DEFAULT FALSE,
  ALTER COLUMN deleted SET DEFAULT FALSE;
COMMIT;

ALTER TABLE persons
  ALTER COLUMN editable DROP DEFAULT,
  ALTER COLUMN editable TYPE bool USING CASE WHEN editable=0 THEN FALSE ELSE TRUE END,
  ALTER COLUMN editable SET DEFAULT FALSE;
COMMIT;

ALTER TABLE workplaces
  ALTER COLUMN now_work DROP DEFAULT,
  ALTER COLUMN now_work TYPE bool USING CASE WHEN now_work=0 THEN FALSE ELSE TRUE END,
  ALTER COLUMN now_work SET DEFAULT FALSE;
COMMIT;
```
</details>

### Settings

For creating regions and alphabeth folders in destination directory add path in settings.ini.
Then run the command:
```
flask folders
```
For creating new user run the command in terminal:
```
export FLASK_APP=app
flask user 'Super Admin' superadmin email@example.com --role=admin --region=main
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


### Start backend

To start a server run the command in terminal:
```
python server.py # for desktop mode; more options see in the server.py
```
DEFAULT_PASSWORD for created user - `88888888`.

### License

This project is licensed under the MIT License.
