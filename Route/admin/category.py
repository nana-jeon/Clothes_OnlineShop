from alembic.script.write_hooks import module

from app import app, db
from sqlalchemy import text
from flask import request, render_template, session, url_for, redirect
from model import User, Product, Order, Category


@app.get('/admin/category')
def category():
    module = 'category'
    categories = Category.query.all()
    return render_template('admin/category/category.html', module=module,categories=categories)


@app.get('/admin/category/form')
def category_form():
    module = 'category'
    categories = Category.query.all()
    status = request.args.get('status')
    return render_template('admin/category/create_category.html', module=module, status=status, categories=categories)


@app.get('/admin/category/category_confirm')  # delete category
def category_confirm():
    module = 'category'
    category_id = int(request.args.get('id'))
    category = Category.query.filter_by(id=category_id).first()
    return render_template('admin/category/delete.html', module=module, category=category)



@app.get('/admin/category/edit')  # edit category
def category_edit():
    module = 'category'
    status = request.args.get('status')
    category = None
    if status == 'edit':
        category_id = int(request.args.get('id'))
        category = Category.query.get(category_id)
    return render_template('admin/category/update.html', module=module, category=category)






# ===================================================================================================================



@app.post('/admin/category/create')
def category_created():
    form = request.form
    category = Category(
        name=form.get('name'),
    )
    db.session.add(category)
    db.session.commit()

    return redirect(url_for('category'))


@app.post('/admin/category/update')
def category_updated():
    form = request.form
    category_id = int(request.args.get('category_id'))
    category = Category.query.get(category_id)
    if category:
        category.name = form.get('name')
        db.session.commit()

    return redirect(url_for('category'))





@app.post('/admin/category/delete')
def category_deleted():
    # Get the category ID from the form (POST)
    category_id = request.form.get('category_id')  # <-- use form, not args
    if not category_id:
        return "Category ID missing!", 400  # safe check

    try:
        category_id = int(category_id)  # convert to int safely
    except ValueError:
        return "Invalid Category ID!", 400

    # fetch category from DB
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()

    # redirect back to your category page
    return redirect(url_for('category'))  # assuming 'category' is your list page














