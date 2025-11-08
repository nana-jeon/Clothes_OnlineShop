from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, index=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    remark = db.Column(db.String(128))
