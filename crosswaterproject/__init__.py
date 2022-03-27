from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
from flask_mail import Mail
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME','livepusher8@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD','wiggle1234')

db = SQLAlchemy(app)
mail = Mail(app)


from crosswaterproject import routes
