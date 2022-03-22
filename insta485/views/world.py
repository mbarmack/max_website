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
    
    with open('output/out_total.txt', 'r') as total_f:
        tot = json.loads(total_f.read())
        print(tot)
        totals = dict(sorted(tot.items(), key=lambda x: x[1], reverse=True))

    country_data = {}
    for country in content:
        if len(content[country]) > 0:
            capitalized = []
            for word in country.split():
                if word != 'of' and word != 'the':
                    capitalized.append(word.capitalize())
                else:
                    capitalized.append(word)

            country_data[' '.join(capitalized)] = len(content[country])
        
    total_data = {}
    for country in totals:
        capitalized = []
        for word in country.split():
            if word != 'of' and word != 'the':
                capitalized.append(word.capitalize())
            else:
                capitalized.append(word)
        
        total_data[' '.join(capitalized)] = totals[country]

    # Normalize for bar width
    minimum = 0
    maximum = max(total_data.values())
    print(minimum)
    print(maximum)
    norm = {}
    photo = {}
    for country in total_data:
        normalized = (total_data[country] - minimum) / (maximum - minimum)
        adjusted = normalized * 600
        adjusted -= 60

        norm[country] = adjusted
        photo[country] = country + ".jpg"
    
    print(json.dumps(norm, indent=2))

    context = {
        'logged_in': logged_in,
        'updated': updated,
        'country_data': country_data,
        'totals': total_data,
        'norm': norm,
        'photo': photo
    }

    return flask.render_template('world.html', **context)