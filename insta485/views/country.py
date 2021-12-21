"""Scraper country view."""

import flask
import insta485
import json

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


    
