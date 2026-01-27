from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.ForeignKey('branch.id'), index=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.String(128))
    branch_table = db.relationship('Branch', backref='branch', lazy=True)
