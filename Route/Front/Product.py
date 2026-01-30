from flask import render_template
from products_list import pro_list
from app import app
from model.product import Product


@app.get('/product')
def home():
    products = Product.query.all()
    return render_template('product.html', products=products, modules=products)

# @app.get('/product')
# def home():
#     products = pro_list
#     return render_template('product.html' , products=products , modules = products)