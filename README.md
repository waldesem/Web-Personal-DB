# StaffSec

StaffSec is a web interface for managing a candidate database.

### The main technology stack used in this project includes:

- Flask;
- Sqlite;
- Vue3;
- Bootstrap 5.

### Installation

To use this project, you will need to have Python 3.10 or higher installed on your local machine.
For installiing the required Python packages run the following command in the terminal:

```
sudo apt install python3 python3-pip python3-venv # if not install venv yet
git clone https://github.com/waldesem/Web-Personal-DB.git
cd Web-Personal-DB/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start backend

To create default values run in  terminal:
```
flask init         # init app
```
To start the application at http://localhost:5000 run the command in terminal:
```
flask run
<!-- waitress-serve --host 127.0.0.1 --port 5000 --threads=8 wsgi:app  # start the waitress server -->
```

Default user for application has name 'superadmin'.
DEFAULT_PASSWORD for all app users is `88888888`. You can change it in config.py file.

### Frontend build

You will need to have Node.js installed on your machine to build and run the TypeScript code. After installation run:
```
npm i
```

To start development node server run the following command in your terminal:

```
npm run dev
```

To build the code in the static directory flask app, first comment/uncomment the lines `server` in /Web-Personal-DB/frontend/src/utilities/utils.ts
Then run the command in terminal:
```
npm run build
```

This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

### License

This project is licensed under the MIT License.
