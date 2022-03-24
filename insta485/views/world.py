"""Scraper main view."""

import flask
import insta485
import json
import pathlib


def normalize(data):
    minimum = 0
    maximum = max(data.values())
    norm = {}
    for country in data:
        normalized = (data[country] - minimum) / (maximum - minimum)
        adjusted = normalized * 520
        norm[country] = adjusted
    
    return norm


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
    total_norm = normalize(total_data)
    norm = normalize(country_data)

    # Generate photo names
    photo = {}
    for country in total_data:
        photo[country] = country + ".jpg"

    # Top tweets
    top_path = pathlib.Path('output/top_tweets.txt')
    with top_path.open('r') as f_in:
        top = json.loads(f_in.read())

    word_path = pathlib.Path('output/top_words.txt')
    with word_path.open('r') as f_in:
        top_words = json.loads(f_in.read())
    
    caps = {}
    for word in top_words:
        cap = word.capitalize()
        caps[cap] = top_words[word]

    minimum = 0
    maximum = max(caps.values())
    cap_norm = {}
    for word in caps:
        normalized = (caps[word] - minimum) / (maximum - minimum)
        adjusted = normalized * 50
        cap_norm[word] = adjusted

    context = {
        'logged_in': logged_in,
        'updated': updated,
        'country_data': country_data,
        'totals': total_data,
        'norm': norm,
        'total_norm': total_norm,
        'top': top,
        'top_words': cap_norm,
        'photo': photo
    }

    return flask.render_template('world.html', **context)