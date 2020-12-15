import tweepy

from .api import init_api

def collect_tweets_by_keyword(keyword, credentials, limit=None):
    '''

    '''

    api = init_api(credentials[0], # consumer_key
                   credentials[1], # consumer_secret
                   credentials[2], # access_token
                   credentials[3]) # access_token_secret

    tweets =[]

    print('\nSTART: Tweet Collection')
    if limit:
        for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='de', tweet_mode='extended').items(limit):
            tweets.append(tweet._json)

            if len(tweets) % 200 == 0:
                print('# of tweets: {}'.format(len(tweets)))
    else:
        for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='de', tweet_mode='extended').items():
            tweets.append(tweet._json)

            if len(tweets) % 200 == 0:
                print('# of tweets: {}'.format(len(tweets)))

    print('END: Tweet Collection')
    print('\nTotal # of tweets: {}'.format(len(tweets)))

    return tweets


def collect_tweets_by_ids(ids, credentials):
    '''

    '''

    api = init_api(credentials[0], # consumer_key
                   credentials[1], # consumer_secret
                   credentials[2], # access_token
                   credentials[3]) # access_token_secret

    tweets =[]

    print('\nSTART: Tweet Collection')
    for id_ in ids:
        try:
            tweet = api.get_status(int(id_), tweet_mode='extended')
            tweets.append(tweet._json)
        except:
            pass
        if len(tweets) % 200 == 0:
            print('# of tweets: {}'.format(len(tweets)))

    print('END: Tweet Collection')
    print('\nTotal # of tweets: {}'.format(len(tweets)))

    return tweets
