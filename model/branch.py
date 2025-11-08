from app import db

class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), nullable=False, index=True) #index=True => unique
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    logo = db.Column(db.String(255), nullable= True)
    description = db.Column(db.String(500))

