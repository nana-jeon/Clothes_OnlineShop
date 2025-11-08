import os
from app import app, db
from sqlalchemy import text
from flask import request, jsonify
from model.product import Product
from werkzeug.utils import secure_filename



@app.get('/product/list')
def product_list():
    return get_product_info(product_id=0)



# select all and filter
@app.get('/product/list/<int:product_id>')
def product_list_by_id(product_id):
    return get_product_info(product_id=product_id)

@app.post('/product/create')
def product_create():
    form = request.form
    file = request.files.get('image')
    image = None

    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['image']
        file_name = f"{form.get('name')}_{secure_filename(file.filename)}"
        file.save(f'./static/images/product/{file_name}')
        image =file_name

    product = Product(
        name=form.get('name'),
        category_id=form.get('category_id'),
        cost=form.get('cost'),
        price=form.get('price'),
        description=form.get('description'),
        image=image,
        stock=form.get('stock')
    )
    db.session.add(product)
    db.session.commit()


    return {
                'message': "product has been created",
                'product': get_product_info(product_id=product.id),
    }, 200

@app.put('/product/update')
def product_update():
    form = request.get_json()
    if not form:
        return {'message': 'no data'}, 400

    is_exist = get_product_info(form.get('product_id'))
    if is_exist.get('message'):
        return {'message': 'product not found ! '}, 400

    product = Product.query.get(form.get('product_id'))

    product.name = form.get('name')
    product.category_id = form.get('category_id')
    product.cost = form.get('cost')
    product.price = form.get('price')
    product.description = form.get('description')
    product.stock = form.get('stock')

    db.session.commit()
    return {
        'message': ' product has been updated',
    },200

@app.delete('/product/delete')
def product_delete():
    data = request.get_json()
    if not data or 'product_id' not in data:
        return {'message': 'no product_id provided'}, 400

    product = Product.query.get(data['product_id'])
    if not product:
        return {'message': 'product not found!'}, 400

    db.session.delete(product)
    db.session.commit()
    return {'message': 'product has been deleted'}, 200






def get_product_info(product_id: int = 0):
    if product_id == 0:
        sql_string = text("select * from product")
        result = db.session.execute(sql_string).fetchall()
        if not result:
            return {'message': 'Product Table is empty'}
        return [dict(row._mapping) for row in result]

    if product_id != 0:
        sql_string = text("select * from product where id = :product_id")
        result = db.session.execute(sql_string , {"product_id" : product_id}).fetchone()

        if not result:
            return {'message': 'Product is not found'}

        return dict(result._mapping)
