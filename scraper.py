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
            clean_line = clean_text(line)
            split = clean_line.split()

            tweet_info[clean_line] = []
            
            countries.append(split)

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
            found = True
            for c_index, c_word in enumerate(country):
                if (t_index + c_index) < len(split_tweet):
                    if split_tweet[t_index + c_index] != c_word:
                        found = False
                else:
                    found = False
            if found:
                tweet_info[' '.join(country)].append(tweet)

def sort_countries(sorted_countries):
    """Sort tweets in country by retweets. Remove duplicates."""
    sort = {}
    for country in sorted_countries:
        s_country = sorted(country[1], key=lambda d: d['retweets'], reverse=True)
        deduplicated = []
        for item in s_country:
            found = False
            for item_2 in deduplicated:
                if item['text'] == item_2['text']:
                    found = True
            if not found:
                deduplicated.append(item)

        sort[country[0]] = deduplicated
    
    return sort


def clean_duplicates(name1, name2):
    """Clean duplicate country names."""
    if tweet_info[name1]:
        for tweet in tweet_info[name1]:
            tweet_info[name2].append(tweet)
    tweet_info.pop(name1)


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
        
        # Account for countries with multiple "names"
        clean_duplicates('uae', 'united arab emirates')
        clean_duplicates('uk', 'united kingdom')
        clean_duplicates('united states', 'united states of america')
        clean_duplicates('usa', 'united states of america')
        clean_duplicates('us', 'united states of america')

        sorted_countries = sorted(tweet_info.items(), key= lambda x: len(x[1]), reverse=True)

        sort = sort_countries(sorted_countries)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        output = {
            'updated': dt_string,
            'data': sort
        }

        out_path = pathlib.Path('output/out.txt')

        with out_path.open('w', encoding='utf-8') as out_file:
            out_file.write(json.dumps(output, indent=2))
        
        time.sleep(21600)



if __name__ == "__main__":
    main()
