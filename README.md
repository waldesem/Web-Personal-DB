# StaffSec

StaffSec is a web interface for managing a candidate database.

### The technology stack used in this project:

- Flask;
- Sqlite3 (or PostgreSQL);
- Vue3 (or Nuxt3);
- Bootstrap 5.

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
Change DATABASE_URI in config.py

### Start backend

To start a server run the command in terminal:
```
python server.py # for debug mode; more options see in the server.py
```
Default admin user for application has name `superadmin`.
DEFAULT_PASSWORD for all created users - `88888888`.

### License

This project is licensed under the MIT License.
