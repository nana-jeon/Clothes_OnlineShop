from app import app, db
from sqlalchemy import text
from flask import request
from model.user import User
from werkzeug.utils import secure_filename
from werkzeug.security import  generate_password_hash

@app.get('/user/list')
def user_list():
    return get_user_info(user_id=0)

# select all and filter
@app.get('/user/list/<int:branch_id>')
def user_list_by_id(user_id):
    return get_user_info(user_id=user_id)

@app.post('/user/create')
def user_create():
    form = request.get_json()

    if not form:
        return 'no data'

    user = User(
        branch_id=form.get('branch_id'),
        username=form.get('username'),
        email=form.get('email'),
        password=generate_password_hash(form.get('password')),
    )
    db.session.add(user)
    db.session.commit()


    return {
                'message': "user has been created",
                'user': get_user_info(user.id),
    }, 200

@app.put('/user/update')
def user_update():
    form = request.get_json()
    if not form:
        return {'message': 'no data'}, 400

    is_exist = get_user_info(form.get('user_id'))
    if is_exist.get('message'):
        return {'message': 'user not found ! '}, 400

    user = User.query.get(form.get('user_id'))
    user.branch_id = form.get('branch_id')
    user.username=form.get('username')
    user.email=form.get('email')

    db.session.commit()

    return {
        'message': 'user has been updated',
    },200

@app.delete('/user/delete')
def user_delete():
    form = request.get_json()

    if not form:
        return {'message' : 'no data'}, 400

    is_exist = get_user_info(form.get('user_id'))
    if is_exist.get('message'):
        return {'message' : 'user not found ! '}, 400

    user = User.query.get(form.get('user_id'))
    db.session.delete(user)
    db.session.commit()

    return {
        'message': 'user has been deleted',
    },200





def get_user_info(user_id: int = 0):
    if user_id == 0:
        sql_string = text("select * from user")
        result = db.session.execute(sql_string).fetchall()
        if not result:
            return {'message': 'User table is empty'}
        return [dict(row._mapping) for row in result]

    if user_id != 0:
        sql_string = text("select * from user where id = :user_id")
        result = db.session.execute(sql_string , {"user_id" : user_id}).fetchone()

        if not result:
            return {'message': 'User is not found'}

        return dict(result._mapping)
