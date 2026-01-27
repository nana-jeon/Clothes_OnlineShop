from alembic.script.write_hooks import module
from app import app, db
from sqlalchemy import text, false
from flask import request, render_template, redirect, url_for, session
from  model import  User
from werkzeug.security import  generate_password_hash


@app.get('/admin/user')  # user page
def user():
    module = 'user'
    users = User.query.all()

    return render_template('admin/user/user.html' , module=module , users=users)



@app.get('/admin/user/form') # add user
def user_form():
    module = 'user'
    status = request.args.get('status')

    return render_template('admin/user/add.html', module=module, status=status, user=user)


@app.get('/admin/user/user_confirm')  # delete user
def user_confirm():
    module = 'user'
    user_id = int(request.args.get('user_id'))
    user = User.query.filter_by(id=user_id).first()
    return render_template('admin/user/delete.html', module=module, user=user)



@app.get('/admin/user/edit')  # delete user
def user_edit():
    module = 'user'
    status = request.args.get('status')
    user = None
    if status == 'edit':
        user_id = int(request.args.get('user_id'))
        user = User.query.get(user_id)
    return render_template('admin/user/update.html', module=module, user=user)



# ========================================================================================================



@app.post('/admin/user/create')
def user_created():
    form = request.form
    user = User(
        branch_id=1,
        username=form.get('username'),
        email=form.get('email'),
        password=generate_password_hash(form.get('password')),
    )
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('user'))

@app.post('/admin/user/update')
def user_updated():
    form = request.form
    user_id = int(request.args.get('user_id'))
    user = User.query.get(user_id)
    if user:
        user.username = form.get('username')
        user.email = form.get('email')
        db.session.commit()

    return redirect(url_for('user'))



@app.post('/admin/user/delete')
def user_deleted():
    user_id = int(request.args.get('user_id'))
    user = User.query.get(user_id)
    if user :
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('user'))
