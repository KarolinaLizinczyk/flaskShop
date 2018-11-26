from flask import Flask
from flask_mail import Mail, Message
import flask_whooshalchemy as wa


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads


from flask_login import LoginManager





app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.cfg')

login_manager = LoginManager(app)

UPLOAD_FOLDER = 'C:/PycharmProjects/FlaskProjects/Shop/app/static/img'


images = UploadSet('images', IMAGES)
configure_uploads(app, images)

db = SQLAlchemy(app)
from .models import ShopProduct


mail = Mail(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

sess = Session()

wa.whoosh_index(app, ShopProduct)
PRODUCTS_PER_PAGE = 2


from . import models, forms, views

