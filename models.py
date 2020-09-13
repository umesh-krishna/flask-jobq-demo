from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    queried_by = db.Column(db.BIGINT, db.ForeignKey('user.id'))
    queried_at = db.Column(db.DateTime)
    word_count = db.Column(db.Integer)


