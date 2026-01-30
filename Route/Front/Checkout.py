from flask import render_template
from app import app

@app.get('/check_out')
def checkout():
    return render_template('check_out.html' , modules = checkout)


