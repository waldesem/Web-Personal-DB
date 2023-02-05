└── flask_personal_app
    ├── config.py               # main app config
    ├── personal.db             # database
    ├── README.md               # readme file
    ├── requirements.txt        # requirements for app
    └── app
        ├── __init__.py         # setup app
        ├── auth.py           # the auth routes for our app
        ├── main.py           # the non-auth routes for our app
        ├── models.py         # our user model
        └── templates
            ├── base.html     # contains common layout and links
            ├── index.html    # show the home page
            ├── login.html    # show the login form
            ├── profile.html  # show the profile page
            └── signup.html   # show the signup form
    