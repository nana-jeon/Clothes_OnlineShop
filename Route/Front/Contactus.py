from flask import render_template
from app import app


@app.get('/contact_us')
def contact_us():
    return render_template('contact_us.html' , modules = contact_us)