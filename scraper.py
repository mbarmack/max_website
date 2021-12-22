#!/usr/bin/env python3

"""Scrapes Twitter for mentions of countries."""

import requests
import pathlib
import re
import json
import threading
import time
from datetime import datetime

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAO2gWQEAAAAA74WzZA8ylP4zI5a1Au5eCOxYX0Q%3Dx2bMqbiR1KmFnxhPRtv6oik0rZdwFD0HlZUavjoPzDEiIR00UD'

user_ids = {}
countries = []
tweet_info = {}


def clean_text(text):
    """Remove non alphanumeric and decapitalize."""
    clean_text = re.sub(r"[^a-zA-Z0-9 ]+", " ", text)

    # Make case-insensitive
    clean_lower = clean_text.casefold()

    if clean_lower[-1] == " ":
        clean_lower = clean_lower[:-1]

    return clean_lower


def load_info():
    """Load info and store in dicts."""
    # Load UIDs
    user_id_path = pathlib.Path('user_ids.txt')
    with user_id_path.open('r', encoding='utf-8') as uid_file:
        for line in uid_file:
            split = line.split()
            user_ids[split[0]] = split[1]

    # Load Countries
    country_names_path = pathlib.Path('country_names.txt')
    with country_names_path.open('r', encoding='utf-8') as country_file:
        for line in country_file:
            names = []
            for name in line.split(','):
                clean_name = clean_text(name)
                split = clean_name.split()
                names.append(split)

            primary_name = ' '.join(names[0])
            primary_name.rstrip()

            tweet_info[primary_name] = []
            
            countries.append(names)


def query_tweets(author, uid, results, i):
    """Query recent tweets from a specific user."""
    # Create API object
    header = {
        "Authorization":f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(
        f"https://api.twitter.com/2/users/{uid}/tweets?tweet.fields=public_metrics&max_results=5",
        headers=header
    )

    response_dict = json.loads(response.text)
    tweets = []
    for tweet_info in response_dict['data']:
        temp = {
            "author": author,
            "id": tweet_info['id'],
            "text": tweet_info['text'],
            "retweets": tweet_info['public_metrics']['retweet_count']
        }
        tweets.append(temp)
    results[i] = tweets




def country_name_search(tweet):
    """Search for country names in tweet."""
    clean_tweet = clean_text(tweet['text'])
    split_tweet = clean_tweet.split()

    for t_index, t_word in enumerate(split_tweet):
        for country in countries:
            primary_name = ' '.join(country[0])
            primary_name.rstrip()
            for name in country:
                found = True
                for c_index, c_word in enumerate(name):
                    if (t_index + c_index) < len(split_tweet):
                        if split_tweet[t_index + c_index] != c_word:
                            found = False
                    else:
                        found = False
                if found and tweet not in tweet_info[primary_name]:
                    tweet_info[primary_name].append(tweet)


def sort_countries(tweet_info):
    """Sort tweets in country by retweets."""
    sort = {}
    for country in tweet_info:
        if tweet_info[country]:
            s_country = sorted(tweet_info[country], key=lambda d: d['retweets'], reverse=True)
        else:
            s_country = []
        sort[country] = s_country
    
    return sort


def main():
    """Main function."""
    # Load and store UID info
    while True:
        load_info()
        
        results = [None] * len(user_ids)
        threads = [None] * len(user_ids)

        for i, ident in enumerate(user_ids.items()):
            print(f"Querying {ident[0]}.....")
            threads[i] = threading.Thread(
                target=query_tweets,
                args=[ident[0], ident[1], results, i]
            )
            threads[i].start()
        
        for thread in threads:
            thread.join()

        tweets = []
        for result in results:
            for tweet in result:
                tweets.append(tweet)

        for tweet in tweets:
            country_name_search(tweet)

        sorted_countries = sort_countries(tweet_info)

        sort = sorted(sorted_countries.items(), key=lambda x: len(x[1]), reverse=True)


        out_data = {}
        for country in sort:
            out_data[country[0]] = country[1]

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        output = {
            'updated': dt_string,
            'data': out_data
        }

        out_path = pathlib.Path('output/out.txt')

        with out_path.open('w', encoding='utf-8') as out_file:
            out_file.write(json.dumps(output, indent=2))
        
        time.sleep(21600)



if __name__ == "__main__":
    main()
