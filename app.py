import dramatiq
from dramatiq.results.backends import RedisBackend
from dramatiq.middleware import CurrentMessage
from dramatiq.results import Results
from flask import Flask
from flask_melodramatiq import RedisBroker
from flask_login import LoginManager
import redis

from models import User

lm = LoginManager()
lm.login_view = "auth.login"
broker = RedisBroker()
dramatiq.set_broker(broker)
result_backend = RedisBackend()
broker.add_middleware(Results(backend=result_backend))
broker.add_middleware(CurrentMessage())
cache = redis.Redis()


@lm.user_loader
def load_user(user_name):
    return User.get(user_name)


def register_blueprints(app):
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from private import private as private_bp
    app.register_blueprint(private_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    lm.init_app(app)
    broker.init_app(app)
    cache = redis.Redis(host=app.config.get('REDIS_HOST', 'localhost'),
                        port=app.config.get('REDIS_PORT', 6379),
                        db=app.config.get('REDIS_DB', 0))

    register_blueprints(app)

    return app
