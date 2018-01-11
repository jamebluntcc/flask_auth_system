# flask auth system

this flask project inspired by [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask) as a template for web application, which aims at develop flask project faster. see [demo](http://120.76.160.204:2323/main/)

# feature
 - Bootstrap 3 and Font Awesome 4 with starter templates
 - Flask-SQLAlchemy with basic User model
 - Easy database migrations with Flask-Migrate
 - Flask-WTForms with login and registration forms
 - Flask-Login for authentication
 - Flask-Bcrypt for password hashing
 - Flask-Admin for manager user auth
 - Flask-mail for email verify
 - Utilizes best practices: Blueprints and Application Factory patterns

# run
 - prepare environment

 I suggest you use [virtualenv](https://pypi.python.org/pypi/virtualenv) if you haven't install virtualenv run `sudo pip install virtualenv` first and execute under code.

```
git clone https://github.com/jamebluntcc/flask_auth_system.git
cd flask_auth_system
virtualenv venv
source venv/bin/activate
sudo pip install -r requirements
```

- init database

```
python manager db init
python manager db migrate
python manager db upgrade
```

-  run it!

```
python manager runserver
```

# change log
 - beta 0.1.0 (12/12/2017)
    - base on cookiecutter-flask init repository.
 - beta 0.1.1 (13/12/2017)
    - add flask admin on auth system.
 - beta 0.1.2 (15/12/2017)
    - add flask mail on auth system to verify user email and update user info page.
 - beta 0.1.2 (11/01/2018)
    - add flask assets and change token confirm.
 
