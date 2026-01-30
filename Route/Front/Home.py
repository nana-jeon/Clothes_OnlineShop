from flask import render_template
from products_list import pro_list
from app import app, db
from model.product import Product



@app.get('/')
def home_page():
    products = Product.query.all()
    return render_template('home.html', products=products)


# @app.route('/')
# def index():
#     products = pro_list
#     return render_template('home.html', products=products, modules='home')
