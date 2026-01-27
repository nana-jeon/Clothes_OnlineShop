from app import app, db
from flask import request
from model.invoice_detail import InvoiceDetail
from sqlalchemy import text


# ---------------------------------------------------------
# Helper: update invoice total whenever details change
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# List invoice details
# ---------------------------------------------------------
@app.get('/invoicedetail/list')
def invoice_detail_list():
    return get_invoice_detail_info(detail_id=0)


@app.get('/invoicedetail/list/<int:detail_id>')
def invoice_detail_by_id(detail_id):
    return get_invoice_detail_info(detail_id=detail_id)


# ---------------------------------------------------------
# Create invoice detail
# ---------------------------------------------------------
@app.post('/invoicedetail/create')
def invoice_detail_create():
    form = request.get_json()
    if not form:
        return {'message': 'No data provided'}, 400

    quantity = float(form.get('quantity', 0))
    price = float(form.get('price', 0))
    amount = quantity * price

    detail = InvoiceDetail(
        invoice_id=form.get('invoice_id'),
        product_id=form.get('product_id'),
        quantity=quantity,
        price=price,
        amount=amount
    )

    db.session.add(detail)
    db.session.commit()

    update_invoice_total(detail.invoice_id)

    return {
        'message': 'Invoice detail has been created',
        'detail': get_invoice_detail_info(detail_id=detail.id)
    }, 200


# ---------------------------------------------------------
# Update invoice detail
# ---------------------------------------------------------
@app.put('/invoicedetail/update')
def invoice_detail_update():
    form = request.get_json()
    if not form or not form.get('id'):
        return {'message': 'No detail id provided'}, 400

    detail = InvoiceDetail.query.get(form.get('id'))
    if not detail:
        return {'message': 'Invoice detail not found'}, 404

    detail.product_id = form.get('product_id', detail.product_id)
    detail.quantity = float(form.get('quantity', detail.quantity))
    detail.price = float(form.get('price', detail.price))
    detail.amount = detail.quantity * detail.price

    db.session.commit()

    update_invoice_total(detail.invoice_id)

    return {
        'message': 'Invoice detail has been updated',
        'detail': get_invoice_detail_info(detail_id=detail.id)
    }, 200


# ---------------------------------------------------------
# Delete invoice detail
# ---------------------------------------------------------
@app.delete('/invoicedetail/delete')
def invoice_detail_delete():
    form = request.get_json()
    if not form or not form.get('id'):
        return {'message': 'No detail id provided'}, 400

    detail = InvoiceDetail.query.get(form.get('id'))
    if not detail:
        return {'message': 'Invoice detail not found'}, 404

    invoice_id = detail.invoice_id

    db.session.delete(detail)
    db.session.commit()

    update_invoice_total(invoice_id)

    return {'message': 'Invoice detail has been deleted'}, 200


# ---------------------------------------------------------
# Get invoice detail
# ---------------------------------------------------------
def get_invoice_detail_info(detail_id: int = 0):
    if detail_id == 0:
        result = db.session.execute(text("SELECT * FROM invoice_detail")).fetchall()
        if not result:
            return {'message': 'Invoice detail table is empty'}
        return [dict(row._mapping) for row in result]

    result = db.session.execute(
        text("SELECT * FROM invoice_detail WHERE id = :id"),
        {"id": detail_id}
    ).fetchone()

    if not result:
        return {'message': 'Invoice detail not found'}

    return dict(result._mapping)
