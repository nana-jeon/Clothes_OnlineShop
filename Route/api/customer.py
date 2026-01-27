from app import app, db
from sqlalchemy import text
from flask import request
from model.customer import Customer
from werkzeug.utils import secure_filename
from werkzeug.security import  generate_password_hash

@app.get('/customer/list')
def customer_list():
    return get_customer_info(customer_id=0)

# select all and filter
@app.get('/customer/list/<int:customer_id>')
def customer_list_by_id(customer_id):
    return get_customer_info(customer_id=customer_id)

@app.post('/customer/create')
def customer_create():
    form = request.get_json()

    if not form:
        return 'no data'

    customer = Customer(
        username=form.get('username'),
        email=form.get('email'),
        password=generate_password_hash(form.get('password')),
        remark=form.get('remark'),
    )
    db.session.add(customer)
    db.session.commit()


    return {
                'message': "customer has been created",
                'user': get_customer_info(customer.id),
    }, 200

@app.put('/customer/update')
def customer_update():
    form = request.get_json()
    if not form:
        return {'message': 'no data'}, 400

    is_exist = get_customer_info(form.get('customer_id'))
    if is_exist.get('message'):
        return {'message': 'customer not found ! '}, 400

    customer = Customer.query.get(form.get('customer_id'))
    customer.username=form.get('username')
    customer.email=form.get('email')
    customer.remark = form.get('remark')

    db.session.commit()

    return {
        'message': 'customer has been updated',
    },200

@app.delete('/customer/delete')
def customer_delete():
    form = request.get_json()

    if not form:
        return {'message' : 'no data'}, 400

    is_exist = get_customer_info(form.get('customer_id'))
    if is_exist.get('message'):
        return {'message' : 'customer not found ! '}, 400

    customer = Customer.query.get(form.get('customer_id'))
    db.session.delete(customer)
    db.session.commit()

    return {
        'message': 'customer has been deleted',
    },200





def get_customer_info(customer_id: int = 0):
    if customer_id == 0:
        sql_string = text("select * from customer")
        result = db.session.execute(sql_string).fetchall()
        if not result:
            return {'message': 'customer table is empty'}
        return [dict(row._mapping) for row in result]

    if customer_id != 0:
        sql_string = text("select * from customer where id = :customer_id")
        result = db.session.execute(sql_string , {"customer_id" : customer_id}).fetchone()

        if not result:
            return {'message': 'customer is not found'}

        return dict(result._mapping)
