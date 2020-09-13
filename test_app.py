import os
import tempfile
import pytest
from app import app
from tests import init_db
from fakeredis import FakeStrictRedis
from tasks import count_words
from redis import Redis
from rq import SimpleWorker, Queue


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200


def test_url_submission_invalid(client):
    rv = client.post('/', data={
        'url': '<an_invalid_url>!'
    })
    assert rv.status_code == 302


def test_url_submission(client):
    rv = client.post('/', data={
        'url': 'google.com'
    })
    assert rv.status_code == 302


def test_worker_fake(client):
    queue = Queue(is_async=False, connection=FakeStrictRedis())
    job = queue.enqueue(count_words, args=('http://www.site.com', None))
    assert job.is_finished


def test_worker(client):
    queue = Queue(connection=Redis())
    task = queue.enqueue(count_words, args=('https://www.facebook.com', None))
    assert len(queue) > 0
    worker = SimpleWorker([queue], connection=queue.connection)
    worker.work(burst=True)  # Runs enqueued job
    assert task.get_id()

