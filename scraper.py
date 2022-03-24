#!/usr/bin/env python3

"""Scrapes Twitter for mentions of countries."""

import requests
import pathlib
import re
import json
import threading
import time
from datetime import datetime
from wordcloud import WordCloud
import random

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

def load_total():
    total_path = pathlib.Path('output/out_total.txt')
    with total_path.open('r') as f_in:
        out_total = json.loads(f_in.read())

    return out_total


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
    

def load_last():
    last_path = pathlib.Path('output/last_ids.txt')
    with last_path.open('r', encoding='utf-8') as f_in:
        last = json.loads(f_in.read())
    
    return last

def query_tweets(author, uid, results, i, last):
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
        if tweet_info['id'] not in last:
            temp = {
                "author": author,
                "id": tweet_info['id'],
                "text": tweet_info['text'],
                "retweets": tweet_info['public_metrics']['retweet_count']
            }
            tweets.append(temp)
    results[i] = tweets


def deduplicater(tweets):
    t = []
    for country in tweets:
        for tweet in tweets[country]:
            t.append(tweet)
    
    deduplicate = []
    for tweet in t:
        dup = False
        ident = tweet['id']
        for de in deduplicate:
            if ident == de['id']:
                dup = True
        if not dup:
            deduplicate.append(tweet)
        
    return deduplicate


def top_tweets(tweets):
    sorted_t = sorted(tweets, key=lambda d: d['retweets'], reverse=True)
    del sorted_t[5:]
    out_path = pathlib.Path('output/top_tweets.txt')
    with out_path.open('w', encoding='utf-8') as out_file:
        out_file.write(json.dumps(sorted_t, indent=2))

def wordcloud(words):
    string_l = []
    for word in words:
        for _ in range(words[word]):
            string_l.append(word)
    
    random.shuffle(string_l)

    string = ' '.join(string_l)
    print(string)

    wordcloud = WordCloud(width = 550, height = 400,
                background_color ='whitesmoke',
                colormap = 'gray',
                min_font_size = 10).generate(string)

    wordcloud.to_file("insta485/static/wordcloud.png")


def top_words(tweets):
    # Load in stopwords
    stop_path = pathlib.Path('stopwords.txt')
    stopw = []
    with stop_path.open('r') as stop_in:
        for word in stop_in.read().split():
            stopw.append(word)
    
    words = {}

    for tweet in tweets:
        for word in tweet['text'].split():
            edit = ""
            if "’s" in word and "’" != word[0]:
                edit = word.replace("’s", '')
            elif "'s" in word and "'" != word[0]:
                edit = word.replace("'s", '')
            else:
                edit = word
            
            print(edit)

            lower = edit.casefold()
            clean = ''.join(c for c in lower if c.isalnum())
            if clean != '':
                not_country = True
                for country in countries:
                    for perm in country:
                        for w in perm:
                            if clean == w:
                                not_country = False

                if clean not in stopw and not_country:
                    if clean in words:
                        words[clean] += 1
                    else:
                        words[clean] = 1

    word_sort = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))
    final = {}
    for word in word_sort:
        if word_sort[word] > 2:
            final[word] = word_sort[word]

    wordcloud(final)

    out_path = pathlib.Path('output/top_words.txt')
    with out_path.open('w') as f_out:
        f_out.write(json.dumps(final, indent=2))


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
        last = load_last()

        results = [None] * len(user_ids)
        threads = [None] * len(user_ids)

        for i, ident in enumerate(user_ids.items()):
            threads[i] = threading.Thread(
                target=query_tweets,
                args=[ident[0], ident[1], results, i, last]
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

        # Record last round of tweets
        last_ids = []
        for country in tweet_info:
            for tweet in tweet_info[country]:
                last_ids.append(tweet['id'])

        out_path = pathlib.Path('output/last_ids.txt')
        with out_path.open('w', encoding='utf-8') as out_file:
            out_file.write(json.dumps(last_ids, indent=2))

        deduplicate = deduplicater(tweet_info)
        # Record top tweets
        top_tweets(deduplicate)

        # Record top words
        top_words(deduplicate)

        sort = sorted(sorted_countries.items(), key=lambda x: len(x[1]), reverse=True)


        out_data = {}
        out_total = load_total()

        for country in sort:
            out_data[country[0]] = country[1]
            num_mentions = len(country[1])

            if num_mentions:
                if country[0] in out_total:
                    out_total[country[0]] += num_mentions
                else:
                    out_total[country[0]] =  num_mentions

        sorted_total = sorted(out_total.items(), key=lambda x: x[1], reverse=True)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        output = {
            'updated': dt_string,
            'data': out_data
        }

        out_path = pathlib.Path('output/out.txt')

        with out_path.open('w', encoding='utf-8') as out_file:
            out_file.write(json.dumps(output, indent=2))
        
        out_tp = pathlib.Path('output/out_total.txt')

        with out_tp.open('w') as f_out:
            f_out.write(json.dumps(out_total, indent=2))
        time.sleep(21600)



if __name__ == "__main__":
    main()
