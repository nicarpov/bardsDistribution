from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'signin'

from app import routes, models
