from app import app, db
from flask import request, jsonify
from sqlalchemy import text
from datetime import datetime, timedelta


# ---------------------------------------------------------
# DAILY SALES (SHOW ALL INVOICES)
# ---------------------------------------------------------
@app.get('/report/sales/daily')
def sales_daily():
    today = datetime.now().date()

    sql = text("""
        SELECT 
            i.id AS invoice_id,
            COALESCE(SUM(d.amount), 0) AS total_sales
        FROM invoice i
        LEFT JOIN invoice_detail d 
            ON i.id = d.invoice_id
        WHERE DATE(i.invoice_date) = :today
        GROUP BY i.id
        ORDER BY i.id
    """)

    result = db.session.execute(sql, {'today': today}).fetchall()
    if not result:
        return {'message': 'No invoices today'}
    return jsonify([dict(row._mapping) for row in result])


# ---------------------------------------------------------
# WEEKLY SALES (SHOW ALL INVOICES)
# ---------------------------------------------------------
@app.get('/report/sales/weekly')
def sales_weekly():
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    sql = text("""
        SELECT 
            i.id AS invoice_id,
            COALESCE(SUM(d.amount), 0) AS total_sales
        FROM invoice i
        LEFT JOIN invoice_detail d 
            ON i.id = d.invoice_id
        WHERE DATE(i.invoice_date) BETWEEN :week_start AND :week_end
        GROUP BY i.id
        ORDER BY i.id
    """)

    result = db.session.execute(sql, {
        'week_start': week_start,
        'week_end': week_end
    }).fetchall()

    if not result:
        return {'message': 'No invoices this week'}

    return jsonify([dict(row._mapping) for row in result])


# ---------------------------------------------------------
# MONTHLY SALES (SHOW ALL INVOICES)
# ---------------------------------------------------------
@app.get('/report/sales/monthly')
def sales_monthly():
    today = datetime.now()
    month_start = today.replace(day=1)
    month_str = month_start.strftime('%Y-%m')

    sql = text("""
        SELECT 
            i.id AS invoice_id,
            COALESCE(SUM(d.amount), 0) AS total_sales
        FROM invoice i
        LEFT JOIN invoice_detail d 
            ON i.id = d.invoice_id
        WHERE strftime('%Y-%m', i.invoice_date) = :month
        GROUP BY i.id
        ORDER BY i.id
    """)

    result = db.session.execute(sql, {'month': month_str}).fetchall()
    if not result:
        return {'message': 'No invoices this month'}

    return jsonify([dict(row._mapping) for row in result])


# ---------------------------------------------------------
# SALES BY CRITERIA
# ---------------------------------------------------------
@app.post('/report/sales/by')
def sales_by_criteria_post():
    data = request.get_json()
    if not data or not data.get('criteria') or not data.get('value'):
        return {'message': 'criteria and value are required'}, 400

    criteria = data['criteria']
    try:
        value = int(data['value'])  # Ensure value is integer
    except ValueError:
        return {'message': 'Value must be a number'}, 400

    if criteria == 'product':
        sql = text("""
            SELECT :value AS product_id, COALESCE(SUM(d.amount), 0) AS total_sales
            FROM (SELECT 1) AS dummy
            LEFT JOIN invoice_detail d ON d.product_id = :value
        """)

    elif criteria == 'category':
        sql = text("""
            SELECT :value AS category_id, COALESCE(SUM(d.amount), 0) AS total_sales
            FROM product p
            LEFT JOIN invoice_detail d ON d.product_id = p.id
            WHERE p.category_id = :value
        """)

    elif criteria == 'user':
        sql = text("""
            SELECT :value AS user_id, COALESCE(SUM(d.amount), 0) AS total_sales
            FROM invoice i
            LEFT JOIN invoice_detail d ON d.invoice_id = i.id
            WHERE i.customer_id = :value
        """)

    else:
        return {'message': 'Invalid criteria'}, 400

    result = db.session.execute(sql, {'value': value}).fetchall()

    # Should always return 1 row due to LEFT JOIN/COALESCE
    return jsonify([dict(row._mapping) for row in result])
