from app import db

class CustomerCart(db.Model):
    __tablename__ = 'customer_cart'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    qty = db.Column(db.Integer)


