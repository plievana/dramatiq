import dramatiq
from dramatiq.results.backends import RedisBackend
from dramatiq.middleware import CurrentMessage
from dramatiq.results import Results
from flask import Flask
from flask_melodramatiq import RedisBroker
import redis

broker = RedisBroker()
dramatiq.set_broker(broker)
result_backend = RedisBackend()
broker.add_middleware(Results(backend=result_backend))
broker.add_middleware(CurrentMessage())
cache = redis.Redis()


@dramatiq.actor
def task():
    print('Snakes appreciate good theatrical preformace.')


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    broker.init_app(app)
    cache = redis.Redis(host='localhost', port=6379, db=0)

    from views import views
    app.register_blueprint(views)

    return app
