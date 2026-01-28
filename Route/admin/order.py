from datetime import datetime

from alembic.script.write_hooks import module
from app import app, db
from sqlalchemy import text, false
from flask import request, render_template, redirect, url_for, session
from model import User, Order
from werkzeug.security import  generate_password_hash


@app.route('/admin/order')
def admin_orders():
    current_time = datetime.now()
    orders = Order.query.all()
    usd_to_khr = 4100  # exchange rate

    total_usd = 0

    for order in orders:
        # Calculate total USD for this order
        order.total_usd = sum(item.qty * item.price for item in order.items)
        # Convert to KHR
        order.total_khr = order.total_usd * usd_to_khr
        order.formatted_khr = "{:,.0f}".format(order.total_khr)

        # Add to total revenue
        total_usd += order.total_usd

    total_khr = total_usd * usd_to_khr
    formatted_total_khr = "{:,.0f}".format(total_khr)

    return render_template(
        'admin/order_management/order.html',
        orders=orders,
        total_orders=len(orders),
        pending_orders=sum(1 for o in orders if o.status=='pending'),
        completed_orders=sum(1 for o in orders if o.status=='completed'),
        total_revenue=total_usd,
        total_usd=total_usd,
        total_khr=total_khr,
        formatted_total_khr=formatted_total_khr,
        current_time=current_time,
    )






@app.get('/admin/order/<int:order_id>')
def order_detail(order_id):
    from model import Order, OrderItem

    usd_to_khr = 4100  # exchange rate
    current_time = datetime.now()

    # Get order
    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order.id).all()

    # Calculate totals per order item and for the order
    order_total_usd = 0
    for item in items:
        item.total = item.qty * item.price
        order_total_usd += item.total

    order.total_usd = order_total_usd
    order.total_khr = order_total_usd * usd_to_khr
    order.formatted_khr = "{:,.0f}".format(order.total_khr)

    return render_template(
        'admin/order_management/order_detail.html',
        order=order,
        items=items,
        current_time=current_time,
    )



