import flask
import json
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

@insta485.app.route('/admin/quote', methods=['POST'])
def add_quote():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    title = flask.request.form['title']
    quote = flask.request.form['quote']

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT postid FROM posts WHERE title=?", (title,)
    )
    postid = cur.fetchall()[0]['postid']

    cur = connection.execute(
        "INSERT INTO quotes (quote, postid)\
         VALUES (?, ?)", (quote, postid)
    )

    connection.commit()

    return flask.redirect(flask.url_for('show_admin'))

@insta485.app.route('/admin/cit', methods=['POST'])
def add_cit():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    title = flask.request.form['title']
    cit = flask.request.form['cit']

    citations = cit.split('\n')
    strip = []

    for cit in citations:
        stripped = cit
        if "\r" in cit:
            stripped = cit[:-1]
        strip.append(stripped)

        print(strip)

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT postid FROM posts WHERE title=?", (title,)
    )
    postid = cur.fetchall()[0]['postid']

    for cit in strip:
        cur = connection.execute(
            "INSERT INTO citations (cit, postid)\
            VALUES (?, ?)", (cit, postid)
        )

    connection.commit()

    return flask.redirect(flask.url_for('show_admin'))

@insta485.app.route('/admin/deletepost/', methods=['POST'])
def delete_post():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    connection = insta485.model.get_db()
    postid = flask.request.form['postid']

    if len(postid) == 0:
        flask.abort(406)

    connection.execute(
        "DELETE FROM paragraphs WHERE postid=?", (postid,)
    )

    connection.execute(
        "DELETE FROM posts WHERE postid=?", (postid,)
    )

    return flask.redirect(flask.url_for('show_admin'))

@insta485.app.route('/admin/deleteparagraph/', methods=['POST'])
def delete_paragraph():
    if 'username' not in flask.session:
        flask.abort(403)
    if flask.session['username'] != "mbarmack":
        flask.abort(403)

    connection = insta485.model.get_db()
    text = flask.request.form['text']
    postid = flask.request.form['postid']

    if len(text) == 0:
        flask.abort(406)

    connection.execute(
        "DELETE FROM paragraphs WHERE paragraph=? AND postid=?", (text, postid)
    )

    return flask.redirect(flask.url_for('show_admin'))