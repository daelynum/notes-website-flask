from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin

# DB initialization
db = SQLAlchemy()
DB_NAME = "database.db"

# the Flask instance creating
app = Flask(__name__)

# admin creating
admin = Admin(app, name='Admin part')


# web app function
def create_app():
    app.config['SECRET_KEY'] = 'krfjrkofjjtf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    # blueprint registration
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, NoteView, UserView
    # check if the DB has been created
    create_database(app)

    login_manager = LoginManager()
    # if the user is not registered, he redirect to the login page
    login_manager.login_view = 'auth.login'
    # link login_manager to app
    login_manager.init_app(app)

    #  admin pages adding

    admin.add_view(UserView(User, db.session))
    admin.add_view(NoteView(Note, db.session))

    # specify the flask how we load the user (by primary key)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# the function of checking the database or, if it does not exist, creating it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # DB creating
        db.create_all(app=app)
        print('Created Database!')
