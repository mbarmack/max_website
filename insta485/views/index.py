"""
Max Barmack homepage
"""
import flask
import insta485

@insta485.app.route('/', methods=['GET'])
def show_about():
    logged_in = False
    if 'username' in flask.session:
        logged_in = True

    context = {
        "logged_in": logged_in
    }
    return flask.render_template('about.html', **context)
