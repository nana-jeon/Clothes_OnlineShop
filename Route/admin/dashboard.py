from alembic.script.write_hooks import module

from app import app, db
from sqlalchemy import text
from flask import request, render_template, session, url_for, redirect
from model import User, Product, Order


@app.get('/admin/')


@app.get('/admin/dashboard')
def dashboard():
    module = 'dashboard'
    return render_template('admin/dashboard/dashboard.html' , module=module,
        total_users=User.query.count(),
        total_orders=Order.query.count(),
        total_products=Product.query.count(),
        total_revenue=18200,
        api_requests_today=1240,
        error_count_today=0,
        recent_logs=[]
    )











