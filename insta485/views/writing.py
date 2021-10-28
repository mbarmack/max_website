"""
Max Barmack Writing Page
"""
import flask
import insta485

@insta485.app.route('/writing/', methods=['GET'])
def show_writing():
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM posts ORDER BY postid DESC"
    )
    posts = cur.fetchall()

    logged_in = False
    if 'username' in flask.session:
        logged_in = True

    context = {
        "posts": posts, 
        "logged_in": logged_in
    }
    return flask.render_template('writing.html', **context)

@insta485.app.route('/writing/<int:postid>/', methods=['GET'])
def show_post(postid):
    logged_in = False
    if 'username' in flask.session:
        logged_in = True

    context = {
        "postid": postid,
        "logged_in": logged_in
    }
    return flask.render_template('post.html', **context)