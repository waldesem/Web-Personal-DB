# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Nuxt3 and TailwindCSS;
- Nitro as a server;
- PostgreSQL;

### Installation

To use this project, you will need to have Node.js version 20 or higher.
For installiing the required packages run commands:
```
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/web_nuxt
npm install
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
CREATE USER staffsec WITH PASSWORD 'staffsec';
GRANT ALL PRIVILEGES ON DATABASE personal TO staffsec;
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

### Build application

To build Nuxt3 as a Server-side Rendering Application run the command in terminal:
```
npx nuxi build
```

### Start backend

To start a server run the command in terminal:
```
HOST=127.0.0.1 PORT=8000 node .output/server/index.mjs
```
DEFAULT_PASSWORD for created user - `88888888`.

### License

This project is licensed under the MIT License.
