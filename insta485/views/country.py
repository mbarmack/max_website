"""Scraper country view."""

import flask
import insta485
import json
import sqlite3

@insta485.app.route('/world/<country>', methods=['GET'])
def show_country(country):
    """Show individual country page."""
    logged_in = False
    if 'username' in flask.session:
        logged_in = True

    country_lower = country.casefold()
    """Show individual country."""
    with open('output/out.txt', 'r') as out_f:
        in_f = json.loads(out_f.read())
        content = in_f['data']


    country_data = content[country_lower]

    context = {
        'logged_in': logged_in,
        'country': country,
        'tweets': country_data
    }

    return flask.render_template('country.html', **context)


@insta485.app.route('/api/graph/', methods=['GET'])
def graph_api():
    if "country" not in flask.request.args:
        raise ValueError("Need to specify a country!")
    
    country = flask.request.args['country'].casefold()

    if not country:
        raise ValueError("Need to specify a country!")
    
    conn = sqlite3.connect('var/tweets.db')
    cursor = conn.cursor()
    print(country)
    results = cursor.execute("SELECT * FROM tweets WHERE country=?", [country]).fetchall()

    data = []

    for elt in results:
        data.append({
            "count": elt[0],
            "country": elt[1],
            "date": elt[2]
        })

    print(data)
    
    return flask.jsonify(data)
