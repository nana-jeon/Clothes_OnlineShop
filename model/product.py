from app import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(128))
    stock = db.Column(db.Numeric(10, 2), default=0)
    description = db.Column(db.String(128))


