from flask import render_template
from products_list import pro_list
from app import app

@app.get('/add_cart')
def add_cart():
    return render_template('add_cart.html' , modules = add_cart)