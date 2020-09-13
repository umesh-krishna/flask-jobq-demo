import redis
from flask_script import Server, Manager
from rq import Connection, Worker
import app
# from uwsgi import app


manager = Manager(app)
manager.add_command(
    'runserver',
    Server(port=5000, use_debugger=True, use_reloader=True))


@manager.command
def runworker():
    redis_url = app.config['RQ_REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['RQ_QUEUES'])
        worker.work()


from flask_rq2 import RQ

rq = RQ()


@manager.command
def worker():
    redis_url = app.config['RQ_REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        default_worker = rq.get_worker()
        default_worker.work(burst=True)


if __name__ == '__main__':
    manager.run()