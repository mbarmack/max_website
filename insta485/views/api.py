import flask
import insta485
import pathlib
import json
import math

@insta485.app.route('/api/v1/writing/', methods=['GET'])
def return_posts():
    connection = insta485.model.get_db()

    search = flask.request.args['search']

    cur = connection.execute(
        "SELECT postid, author, title\
        FROM posts",
    )
    posts = cur.fetchall()
    posts.reverse()

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

    # Get and set quote
    cur = connection.execute(
        "SELECT quote, quoteid FROM quotes WHERE postid=?", (postid,)
    )

    quote = cur.fetchall()
    if len(quote) is 0:
        quote = None
    else:
        quote = quote[0]

    #Get and set citations
    cur = connection.execute(
        "SELECT cit, citid FROM citations WHERE postid=?", (postid,)
    )
    cits = cur.fetchall()

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

    if not quote:
        context = {
            "author": post['author'],
            "body": paragraphs,
            "comments": comments,
            "citations": cits,
            "created": post['created'],
            "logged_in": logged_in,
            "logname": logname,
            "postid": post['postid'],
            "quote": "",
            "title": post['title']
        }
    else:
        context = {
            "author": post['author'],
            "body": paragraphs,
            "comments": comments,
            "citations": cits,
            "created": post['created'],
            "logged_in": logged_in,
            "logname": logname,
            "postid": post['postid'],
            "quote": quote['quote'],
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

@insta485.app.route('/api/v1/map/', methods=['GET'])
def get_map():
    map_data = {}
    map_path = pathlib.Path('output/out.txt')
    with map_path.open('r') as map_in:
        map_data = json.loads(map_in.read())
    
    lat_lon_path = pathlib.Path('country_lat_lon.txt')
    lat_lon = {}
    with lat_lon_path.open('r') as lat_in:
        for row in lat_in.read().split('\n'):
            country, lat, lon = row.split('|')
            lat_lon[country.casefold()] = {
                'lat': lat,
                'lon': lon
            }
    
    map_counts = {}
    
    for country in map_data['data']:
        count = len(map_data['data'][country])
        count *= 15000
        if count > 0:
            name = ""
            temp = []
            for word in country.split():
                if word != 'of' and word != 'the':
                    temp.append(word.capitalize())
                else:
                    temp.append(word)
                
            name = ' '.join(temp)
                
            map_counts[country] = {
                "name": name,
                "count": count + 50000,
                "lat": lat_lon[country]['lat'],
                "lon": lat_lon[country]['lon']
            }

    context = {
        "map_counts": map_counts
    }

    return flask.make_response(flask.jsonify(context), 200)