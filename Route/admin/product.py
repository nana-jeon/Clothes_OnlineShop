import os
from werkzeug.utils import secure_filename
from app import app, db
from flask import request, render_template, url_for, redirect, current_app
from model import Product, Category

# Absolute upload folder path
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/images/product')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------- Product List ----------------------
@app.get('/admin/product')
def product_form():
    module = 'product'
    products = Product.query.all()

    # Convert numeric fields to float for Jinja
    for prod in products:
        prod.cost = float(prod.cost) if prod.cost is not None else 0.0
        prod.price = float(prod.price) if prod.price is not None else 0.0
        prod.stock = float(prod.stock) if prod.stock is not None else 0.0

    return render_template('admin/product/product.html', module=module, products=products)


# ---------------------- Add Product ----------------------
@app.get('/admin/product/add')
def add_product():
    module = 'product'
    status = request.args.get('status')
    all_products = Product.query.all()
    categories = Category.query.all()

    return render_template(
        'admin/product/create_product.html',
        module=module,
        status=status,
        products=all_products,
        categories=categories
    )


# ---------------------- Delete Product Confirm ----------------------
@app.get('/admin/product/product_confirm')
def product_confirm():
    module = 'product'
    product_id = request.args.get('product_id', type=int)
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template('admin/product/delete.html', module=module, product=product)


# ---------------------- Edit Product ----------------------
@app.get('/admin/product/edit')
def product_edit():
    module = 'product'
    status = request.args.get('status')
    categories = Category.query.all()
    product = None
    if status == 'edit':
        product_id = request.args.get('product_id', type=int)
        product = Product.query.get(product_id)
        if not product:
            return "Product not found", 404

    return render_template('admin/product/update.html', module=module, product=product, categories=categories)


# ---------------------- Create Product ----------------------
@app.post('/admin/product/create')
def product_created():
    form = request.form
    image_file = request.files.get('image')

    # Save uploaded image
    image_filename = None
    if image_file and image_file.filename != '':
        image_filename = f"{form.get('name')}_{secure_filename(image_file.filename)}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

    # Create product object
    new_product = Product(
        category_id=int(form.get('category')),
        name=form.get('name'),
        cost=float(form.get('cost')) if form.get('cost') else 0.0,
        price=float(form.get('price')) if form.get('price') else 0.0,
        stock=int(form.get('stock')) if form.get('stock') else 0,
        description=form.get('description'),
        image=image_filename
    )

    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('product_form'))


# ---------------------- Update Product ----------------------
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
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_filename = f"{secure_filename(product.name)}_{secure_filename(image_file.filename)}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

        # Delete old image if exists
        if product.image:
            old_path = os.path.join(UPLOAD_FOLDER, product.image)
            if os.path.exists(old_path):
                os.remove(old_path)

        product.image = image_filename

    db.session.commit()
    return redirect(url_for('product_form'))


# ---------------------- Delete Product ----------------------
@app.post('/admin/product/delete')
def product_deleted():
    product_id = request.form.get('product_id')
    if product_id:
        product = Product.query.get(int(product_id))
        if product:
            db.session.delete(product)
            db.session.commit()

    return redirect(url_for('product_form'))
