from app import app, db
from sqlalchemy import text
from flask import request
from model.branch import Branch
from werkzeug.utils import secure_filename

@app.get('/branch/list')
def branch_list():
    return get_branch_info(branch_id=0)

# select all and filter
@app.get('/branch/list/<int:branch_id>')
def branch_list_by_id(branch_id):
    return get_branch_info(branch_id=branch_id)

@app.post('/branch/create')
def branch_create():
    form = request.form
    file = request.files.get('logo')
    logo = None

    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['logo']
        file_name = f"{form.get('name')}_{form.get('phone')}_{secure_filename(file.filename)}"
        file.save(f'./static/images/branch/{file_name}')
        logo =file_name



    branch = Branch(
        name=form.get('name'),
        phone=form.get('phone'),
        address=form.get('address'),
        description=form.get('description'),
        logo=logo,
    )
    db.session.add(branch)
    db.session.commit()


    return {
                'message': "branch has been created",
                'branch': get_branch_info(branch_id=branch.id),
    }, 200

@app.put('/branch/update')
def branch_update():
    form = request.get_json()
    if not form:
        return {'message': 'no data'}, 400

    is_exist = get_branch_info(form.get('branch_id'))
    if is_exist.get('message'):
        return {'message': 'branch not found ! '}, 400

    branch = Branch.query.get(form.get('branch_id'))
    branch.name = form.get('name')
    branch.phone = form.get('phone')
    branch.address = form.get('address')
    branch.description = form.get('description')

    db.session.commit()
    return {
        'message': 'Branch has been updated',
    },200

@app.delete('/branch/delete')
def branch_delete():
    form = request.get_json()

    if not form:
        return {'message' : 'no data'}, 400

    is_exist = get_branch_info(form.get('branch_id'))
    if is_exist.get('message'):
        return {'message' : 'branch not found ! '}, 400

    branch = Branch.query.get(form.get('branch_id'))
    db.session.delete(branch)
    db.session.commit()

    return {
        'message': 'branch has been deleted',
    },200





def get_branch_info(branch_id: int = 0):
    if branch_id == 0:
        sql_string = text("select * from branch")
        result = db.session.execute(sql_string).fetchall()
        if not result:
            return {'message': 'Branch Table is empty'}
        return [dict(row._mapping) for row in result]

    if branch_id != 0:
        sql_string = text("select * from branch where id = :branch_id")
        result = db.session.execute(sql_string , {"branch_id" : branch_id}).fetchone()

        if not result:
            return {'message': 'Branch is not found'}

        return dict(result._mapping)
