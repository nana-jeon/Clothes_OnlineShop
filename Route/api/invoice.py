from app import app, db
from sqlalchemy import text
from model.invoice import Invoice
from flask import request, jsonify
from datetime import datetime
from decimal import Decimal




@app.get('/invoice/list')
def invoice_list():
    return get_invoice_info(invoice_id=0)


@app.get('/invoice/list/<int:invoice_id>')
def invoice_list_by_id(invoice_id):
    return get_invoice_info(invoice_id=invoice_id)



@app.post('/invoice/create')
def create_invoice():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data "}), 400

    customer_id = data.get("customer_id")
    invoice_date = data.get("invoice_date")
    total_amount = data.get("total_amount")

    if not customer_id or not invoice_date or total_amount is None:
        return jsonify({"message": "customer_id, invoice_date and total_amount are required"}), 400

    # Convert string date to datetime
    invoice_date = datetime.fromisoformat(invoice_date)

    # Convert to Decimal for Numeric column
    total_amount = Decimal(total_amount)

    new_invoice = Invoice(
        customer_id=customer_id,
        invoice_date=invoice_date,
        total_amount=total_amount
    )

    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({"message": "invoice has been created", "invoice_id": new_invoice.id})



@app.put('/invoice/update')
def invoice_update():
    form = request.get_json()
    if not form or not form.get('id'):
        return {'message': 'No invoice id provided'}, 400

    invoice = Invoice.query.get(form.get('id'))
    if not invoice:
        return {'message': 'Invoice not found'}, 404

    # Update customer
    if form.get('customer_id'):
        invoice.customer_id = form.get('customer_id')

    # Update invoice date
    if form.get('invoice_date'):
        try:
            invoice.invoice_date = datetime.fromisoformat(form.get('invoice_date'))
        except ValueError:
            return {'message': 'Invalid date format, use YYYY-MM-DDTHH:MM:SS'}, 400

    # total_amount is always managed by invoice_detail
    # But allow manual override if provided
    if form.get('total_amount') is not None:
        invoice.total_amount = float(form.get('total_amount'))

    db.session.commit()

    return {
        'message': 'Invoice has been updated',
        'invoice': get_invoice_info(invoice_id=invoice.id)
    }, 200



@app.delete('/invoice/delete')
def invoice_delete():
    form = request.get_json()

    if not form:
        return {'message' : 'no data'}, 400

    is_exist = get_invoice_info(form.get('invoice_id'))
    if is_exist.get('message'):
        return {'message' : 'invoice not found ! '}, 400

    customer = Invoice.query.get(form.get('invoice_id'))
    db.session.delete(customer)
    db.session.commit()

    return {
        'message': 'invoice has been deleted',
    },200



def update_invoice_total(invoice_id):
    total = db.session.execute(text("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM invoice_detail
        WHERE invoice_id = :invoice_id
    """), {'invoice_id': invoice_id}).scalar()

    db.session.execute(text("""
        UPDATE invoice
        SET total_amount = :total
        WHERE id = :invoice_id
    """), {'total': total, 'invoice_id': invoice_id})

    db.session.commit()


def get_invoice_info(invoice_id: int = 0):
    if invoice_id == 0:
        sql_string = text("SELECT * FROM invoice")
        result = db.session.execute(sql_string).fetchall()
        if not result:
            return {'message': 'Invoice table is empty'}

        invoices = []
        for row in result:
            inv = dict(row._mapping)

            customer = db.session.execute(
                text("SELECT username FROM customer WHERE id = :customer_id"),
                {"customer_id": inv['customer_id']}
            ).fetchone()

            inv['customer_name'] = customer._mapping['username'] if customer else None
            invoices.append(inv)

        return invoices

    sql_string = text("SELECT * FROM invoice WHERE id = :invoice_id")
    result = db.session.execute(sql_string, {"invoice_id": invoice_id}).fetchone()
    if not result:
        return {'message': 'Invoice not found'}

    inv = dict(result._mapping)

    customer = db.session.execute(
        text("SELECT username FROM customer WHERE id = :customer_id"),
        {"customer_id": inv['customer_id']}
    ).fetchone()

    inv['customer_name'] = customer._mapping['username'] if customer else None
    return inv


