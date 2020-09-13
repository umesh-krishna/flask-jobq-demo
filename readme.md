# Flask | Task Queue Demo

Technologies Used
  - Python 3.6
  - Flask 1.1.2
  - SQLAlchemy
  - FlaskRQ-2
  - Redis 4.0.9
  - SQLite

# Installation

  - Clone this repository
  - Install dependency packages 
    `pip install -r requirements.txt`
  - Install and Start Redis-Server
    `sudo apt install redis-server`
    `sudo systemctl start redis.service`
  - Setup Database
    `flask db init`
    `flask db migrate`
    `flask db upgrade`
  - Run Worker Process
    `rq worker` or `flask rq worker`
  - Run development Server
    `python app.py 0.0.0.0:5000`


### Unit Test using Pytest

From the Project root directory, run: `pytest`

