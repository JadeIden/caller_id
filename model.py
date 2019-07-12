import datetime

from app import db


class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.Binary, nullable=False)
    last_access = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Name {self.text}>"
