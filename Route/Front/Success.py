from flask import render_template

from app import app


@app.get('/successful')
def successful():
    return render_template('successful.html' , modules = successful)