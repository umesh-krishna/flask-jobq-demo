from settings import *
from flask import render_template
from flask import request, flash
from flask_login import login_user
from flask import session, redirect, url_for
from flask_rq2 import RQ
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test3.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = b'secret_key/'
app.config['RQ_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['RQ_QUEUES'] = ['default']
app.config['RQ_ASYNC'] = True
QUEUES = ['default']
rq = RQ(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import models
import users
import tasks


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@app.route('/test/', methods=['GET', 'POST'])
def test():
    return 'TEST'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            queries = models.Query.query.filter_by(queried_by=session['user_id']).order_by(models.Query.id.desc())
            return render_template('index.html', queries=queries)
    else:
        url = request.form.get('url', '')
        if url:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = "http://{}".format(url)
            tasks.count_words.queue(url, session.get('user_id'))
        return redirect(url_for('index'))


@app.route('/signup/', methods=['POST'])
def signup():
    error = users.check_signup_form_errors(request)
    if not error:
        users.create_user(request)
        flash('Your account has been created. Login now.')
    else:
        flash('ERROR! {}'.format(error))
    return redirect(url_for('index'))


@app.route('/login/', methods=['POST'])
def login():
    user = users.authenticate(request.form['username'], request.form['password'])
    if user:
        login_user(user)
        session['logged_in'] = True
        session['username'] = user.username
        session['user_id'] = user.id
    else:
        flash('Invalid Credentials! Try again.')
    return redirect(url_for('index'))


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
