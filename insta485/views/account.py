import hashlib
import uuid
import flask
import insta485

def salt_and_hash(password):
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string

@insta485.app.route('/accounts/login/', methods=['GET'])
def show_login():
    """Return login page"""
    target = flask.request.args.get('target')
    if 'username' in flask.session:
        return flask.render_template(flask.url_for(target))
    context = {
        "target": target
    }
    return flask.render_template("login.html", **context)

@insta485.app.route('/accounts/create/', methods=['GET'])
def show_create():
    """Create Account"""
    target = flask.request.args.get('target')
    if 'username' in flask.session:
        return flask.render_template(flask.url_for(target))
    context = {
        "target": target
    }
    return flask.render_template("create.html", **context)



@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def logout():
    """Log user out"""
    target = flask.request.args.get('target')
    flask.session.clear()
    return flask.redirect(target)

@insta485.app.route('/accounts/login/', methods=['POST'])
def process_login():
    target = flask.request.args.get('target')

    if target is None:
        target = flask.url_for('show_about')

    connection = insta485.model.get_db()

    if flask.request.form['password'] is None \
        or flask.request.form['username'] is None:
            flask.abort(406)

    cur = connection.execute(
        "SELECT password \
        FROM users \
        WHERE username=?", (flask.request.form['username'],)
    )
    db_pw = cur.fetchall()
    if db_pw is None:
        flask.abort(403)
    db_pw = db_pw[0]['password']

    itemized_db_pw = db_pw.split('$')
    db_salt = itemized_db_pw[1]
    hash_obj = hashlib.new('sha512')

    password_salted = db_salt + flask.request.form['password']
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    
    if itemized_db_pw[2] != password_hash:
        flask.abort(403)

    cur = connection.execute(
        "SELECT username \
            FROM users \
            WHERE username=?", (flask.request.form['username'],)
    )
    users = cur.fetchall()
    for user in users:
        if flask.request.form['username'] == user['username']:
            flask.session['username'] = flask.request.form['username']
            flask.session['password'] = db_pw
            return flask.redirect(target)
    flask.abort(403)

@insta485.app.route('/accounts/create/', methods=['POST'])
def process_creation():
    target = flask.request.args.get('target')
    if target is None:
        target = flask.url_for('show_about')
    
    connection = insta485.model.get_db()

    username = flask.request.form['username']
    password = flask.request.form['password']
    password_confirm = flask.request.form['password2']

    if password != password_confirm:
        flask.abort(406)

    if username is None or password is None:
        flask.abort(406)
    else:
        cur = connection.execute("SELECT username FROM users")
        users = cur.fetchall()
        for user in users:
            if user['username'] == username:
                print("Username already exists. Exiting with abort(409)")
                flask.abort(409)

    password_db_string = salt_and_hash(password)

    connection.execute(
        "INSERT INTO users(username, password) \
         VALUES (?, ?)",
        (username, password_db_string)
    )

    flask.session['username'] = username
    flask.session['password'] = password_db_string
    return flask.redirect(target)