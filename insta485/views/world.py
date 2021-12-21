"""Scraper main view."""

import flask
import insta485
import json

@insta485.app.route('/world/', methods=['GET'])
def show_world():
    """Show world news page."""
    logged_in = False
    if 'username' in flask.session:
        logged_in = True

    with open('output/out.txt', 'r') as out_f:
        in_f = json.loads(out_f.read())
        updated = in_f['updated']
        content = in_f['data']

    
    country_data = {}
    for country in content:
        if len(content[country]) > 0:
            capitalized = []
            for word in country.split():
                if word != 'of':
                    capitalized.append(word.capitalize())
                else:
                    capitalized.append(word)

            country_data[' '.join(capitalized)] = len(content[country])

    context = {
        'logged_in': logged_in,
        'updated': updated,
        'country_data': country_data
    }

    return flask.render_template('world.html', **context)