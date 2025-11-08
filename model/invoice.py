from app import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    invoice_date = db.Column(db.DateTime, default=datetime, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)