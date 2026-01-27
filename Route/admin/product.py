import os
from itertools import product

from alembic.script.write_hooks import module
from werkzeug.utils import secure_filename

from app import app, db
from sqlalchemy import text
from flask import request, render_template, session, url_for, redirect, Flask, current_app
from model import User, Product, Order, Category


UPLOAD_FOLDER = './static/images/users'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get('/admin/product')
def product_form():
    module = 'product'
    products = Product.query.all()

    # Convert Numeric fields to float for Jinja
    for p in products:
        p.cost = float(p.cost) if p.cost is not None else 0.0
        p.price = float(p.price) if p.price is not None else 0.0
        p.stock = float(p.stock) if p.stock is not None else 0.0

    return render_template('admin/product/product.html', module=module, products=products)


@app.get('/admin/product/add')
def add_product():
    module = 'product'
    status = request.args.get('status')
    product = Product.query.all()
    categories = Category.query.all()

    return render_template('admin/Product/create_product.html', module=module, status=status, products=product, categories=categories)



@app.get('/admin/product/product_confirm')  # delete product
def product_confirm():
    module = 'product'
    product_id = int(request.args.get('product_id'))
    product = Product.query.filter_by(id=product_id).first()
    return render_template('admin/Product/delete.html', module=module, product=product)



@app.get('/admin/product/edit')  # edit product
def product_edit():
    module = 'product'
    status = request.args.get('status')
    categories = Category.query.all()
    product = None
    if status == 'edit':
        product_id = int(request.args.get('product_id'))
        product = Product.query.get(product_id)
    return render_template('admin/Product/update.html', module=module, product=product, categories=categories)





# ===================================================================================================================


@app.post('/admin/product/create')
def product_created():
    """Handle product creation"""
    form = request.form
    image_file = request.files.get('image')

    # Save uploaded image
    image_filename = None
    if image_file and image_file.filename != '':
        image_filename = f"{form.get('name')}_{secure_filename(image_file.filename)}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

    # Create Product object
    product = Product(
        category_id=int(form.get('category')),  # make sure dropdown has name="category"
        name=form.get('name'),
        cost=float(form.get('cost')) if form.get('cost') else 0.0,
        price=float(form.get('price')) if form.get('price') else 0.0,
        stock=int(form.get('stock')) if form.get('stock') else 0,
        description=form.get('description'),
        image=image_filename
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for('product_form'))  # redirect to product list




@app.post('/admin/product/update')
def product_updated():
    form = request.form
    product_id = form.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404

    # Update text fields
    product.name = form.get('name') or product.name
    product.category_id = int(form.get('category')) if form.get('category') else product.category_id
    product.cost = float(form.get('cost')) if form.get('cost') else product.cost
    product.price = float(form.get('price')) if form.get('price') else product.price
    product.stock = int(float(form.get('stock'))) if form.get('stock') else product.stock
    product.description = form.get('description') or product.description

    # Image upload
    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        # Ensure upload folder exists
        upload_folder = os.path.join(current_app.root_path, 'static/images/product')
        os.makedirs(upload_folder, exist_ok=True)

        # Build a safe filename
        image_filename = f"{secure_filename(product.name)}_{secure_filename(image_file.filename)}"
        image_path = os.path.join(upload_folder, image_filename)

        # Save the new image
        image_file.save(image_path)

        # Delete old image if exists
        if product.image:
            old_path = os.path.join(upload_folder, product.image)
            if os.path.exists(old_path):
                os.remove(old_path)

        # Update product image
        product.image = image_filename

    db.session.commit()
    return redirect(url_for('product_form'))




@app.post('/admin/product/delete')
def product_deleted():
    # Get product_id from POST form, not args
    product_id = request.form.get('product_id')
    if product_id:
        product = Product.query.get(int(product_id))
        if product:
            db.session.delete(product)
            db.session.commit()

    return redirect(url_for('product_form'))



















