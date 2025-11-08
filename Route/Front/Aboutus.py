from flask import render_template

def register_aboutus_routes(app):
    @app.get('/about_us')
    def about_us():
        return render_template('about_us.html', modules='about_us')
