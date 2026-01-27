from flask import render_template
from app import app


@app.get('/about_us')
def about_us():
    return render_template('about_us.html' )


