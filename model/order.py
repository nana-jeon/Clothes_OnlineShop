from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # ✅ FIXED
    status = db.Column(db.String(128))

    total_usd = db.Column(db.Float, nullable=False, default=0)
    total_khr = db.Column(db.Float, nullable=False, default=0)

    items = db.relationship('OrderItem', backref='order', lazy=True)
    customer = db.relationship('Customer', backref='orders', lazy=True)

    @property
    def customer_name(self):
        if self.customer:  # registered user
            return self.customer.username
        elif self.first_name or self.last_name:  # guest checkout
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return 'Guest'




