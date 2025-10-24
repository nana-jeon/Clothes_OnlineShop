from flask import render_template
from products_list import pro_list
from app import app

@app.get('/product')
def home():
    products = pro_list
    return render_template('product.html' , products=products , modules = products)