import flask
import insta485

@insta485.app.route('/admin/', methods=['GET'])
def show_admin():
    if 'username' in flask.session:
        if flask.session['username'] == "mbarmack":
            return flask.render_template('admin.html')
    flask.abort(403)

@insta485.app.route('/admin/post', methods=['POST'])
def add_post():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    title = flask.request.form['title']
    author = flask.request.form['author']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT COUNT(title) FROM posts WHERE title=?", (title,)
    )
    duplicate = cur.fetchall()[0]['COUNT(title)']

    if duplicate > 0:
        flask.abort(409)


    cur = connection.execute(
        "INSERT INTO posts (author, title)\
         VALUES (?, ?)", (author, title)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_admin'))

@insta485.app.route('/admin/text', methods=['POST'])
def add_text():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    title = flask.request.form['title']
    paragraph = flask.request.form['paragraph']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT postid FROM posts WHERE title=?", (title,)
    )
    postid = cur.fetchall()[0]['postid']

    cur = connection.execute(
        "INSERT INTO paragraphs (paragraph, postid)\
         VALUES (?, ?)", (paragraph, postid)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_admin'))