from alembic.script.write_hooks import module
from app import app, db
from sqlalchemy import text, false
from flask import request, render_template, redirect, url_for, session, flash, jsonify
from  model import  User, user
from werkzeug.security import generate_password_hash, check_password_hash


@app.get('/login')  # user page
def admin_login():

    return render_template('admin/login.html')





# @app.post('/do_login')
# def do_login():
#
#     form = request.form
#     email = form.get('email')
#     password = form.get('password')
#     user = User.query.filter_by(email=email).first()
#
#     if not user:
#         return redirect(url_for('login'))
#     hashed_password = user.password
#     if check_password_hash(hashed_password, password):
#         session['user_id'] = user.id
#         session['username'] = user.username
#         session['email'] = user.email
#         return redirect(url_for('dashboard'))


@app.post('/do_login')
def do_login():
    form = request.form
    email = form.get('email')
    password = form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        # Show alert for user not found
        error = "Email not found."
        return render_template('admin/login.html', error=error)

    hashed_password = user.password
    if check_password_hash(hashed_password, password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        return redirect(url_for('dashboard'))
    else:
        # Show alert for wrong password
        error = "Incorrect password."
        return render_template('admin/login.html', error=error)





@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


