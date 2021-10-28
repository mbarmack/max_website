import flask
import insta485

@insta485.app.route('/api/v1/writing/', methods=['GET'])
def return_posts():
    connection = insta485.model.get_db()

    search = flask.request.args['search']

    cur = connection.execute(
        "SELECT postid, author, title\
        FROM posts",
    )
    posts = cur.fetchall()

    context = {
        "posts": posts
    }

    return flask.make_response(flask.jsonify(context), 200)


@insta485.app.route('/api/v1/writing/<int:postid>/', methods=['GET'])
def return_post(postid):
    connection = insta485.model.get_db()

    logged_in = False
    logname = "none"
    if 'username' in flask.session:
        logged_in = True
        logname = flask.session['username']


    #Get and set post data
    cur = connection.execute(
        "SELECT * FROM posts WHERE postid=?", (postid,)
    )
    post = cur.fetchall()[0]

    #Get and set paragraphs
    cur = connection.execute(
        "SELECT paragraph, paragraphid FROM paragraphs WHERE postid=?", (postid,)
    )
    paragraphs = cur.fetchall()

    #Get and set comment data
    cur = connection.execute(
        "SELECT commentid, owner, author, text, postid \
         FROM comments WHERE postid=?",
        (postid,)
    )
    comments = cur.fetchall()

    for comment in comments:
        if 'username' in flask.session:
            if comment['owner'] == flask.session['username']:
                comment['logname_owns_this'] = True
            else:
                comment['logname_owns_this'] = False

    context = {
        "author": post['author'],
        "body": paragraphs,
        "comments": comments,
        "created": post['created'],
        "logged_in": logged_in,
        "logname": logname,
        "postid": post['postid'],
        "title": post['title']
    }
    #Return JSON file
    return flask.make_response(flask.jsonify(context), 200)

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    if 'username' not in flask.session:
        flask.abort(403)

    connection = insta485.model.get_db()

    postid = flask.request.args['postid']
    author = flask.request.json['author']
    text = flask.request.json['text']

    if text == "" or author == "":
        flask.abort(409)
    
    cur = connection.execute(
        "INSERT INTO comments (author, owner, text, postid) \
         VALUES (?, ?, ?, ?)",
        (author, flask.session['username'], text, postid)
    )

    cur = connection.execute("SELECT * FROM comments ORDER BY commentid DESC")
    comment = cur.fetchall()[0]

    if 'username' in flask.session:
        if comment['owner'] == flask.session['username']:
            comment['logname_owns_this'] = True
        else:
            comment['logname_owns_this'] = False

    response = {
        "commentid": comment['commentid'],
        "logname_owns_this": comment['logname_owns_this'],
        "owner": comment['owner'],
        'author': comment['author'],
        'text': comment['text'],
    }

    connection.commit()

    return flask.make_response(flask.jsonify(response), 201)

@insta485.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Removes comment from database"""
    if 'username' not in flask.session:
        flask.abort(403)

    connection = insta485.model.get_db()

    connection.execute(
        "DELETE FROM comments WHERE commentid=?", (commentid,)
    )

    return flask.make_response('', 204)

@insta485.app.route('/api/v1/users/', methods=['POST'])
def get_users():
    if flask.request.json['sender'] != "admin":
        flask.abort(403)
    if flask.request.json['key'] != "gh576nl5ttn9i":
        flask.abort(403)

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username FROM users"
    )

    users = cur.fetchall()

    context = {
        "users": users
    }

    return flask.make_response(flask.jsonify(context), 200)