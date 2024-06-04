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

To create application run the following command in your terminal:
```
flask init         # init environments
flask create       # create default values
```
To start the application at http://localhost:5000 run the following command in your terminal:
```
flask run          # start the application
```

Default user for application has name 'superadmin'.
DEFAULT_PASSWORD for all app users is `88888888`. You can change it in config.py file.
Change it in first login to application.

### Frontend build

You will also need to have Node.js installed on your machine to build and run the TypeScript code.
After installing Node.js, you can install the required npm packages by running in your webapp directory the following command in your terminal:

```
npm i
```

To start development node server run the following command in your terminal:

```
npm run dev
```

To build the code in the static directory flask app, first comment/uncomment the lines `server` in /Web-Personal-DB/frontend/src/utilities/utils.ts
Then run the following command in your terminal:

```
npm run build
```

This will compile the TypeScript code and output the JavaScript and CSS files in the static directory '/backend/app/static'.

### License

This project is licensed under the MIT License.
