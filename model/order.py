from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime, nullable=False)
    status = db.Column(db.String(128))




