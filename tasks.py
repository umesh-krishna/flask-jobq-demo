import requests
from flask_rq2 import RQ
from app import app
import models
from datetime import datetime
from app import db
import sys
import html2text


rq = RQ(app)


@rq.job
def count_words(url, user_id):
    query = models.Query(url=url, queried_by=user_id, queried_at=datetime.now())
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        count = None
    else:
        # Extract text contents
        h = html2text.HTML2Text()
        h.ignore_links = True
        text_content = h.handle(response.text)  # ignore html tags, scripts and styles
        text_content = ''.join(e for e in text_content if (e.isalnum() or e == ' '))  # remove special characters
        count = len(text_content.split())
        print(text_content.split(), file=sys.stdout)
    query.word_count = count
    db.session.add(query)
    db.session.commit()

