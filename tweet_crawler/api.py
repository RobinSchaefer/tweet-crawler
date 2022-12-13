import tweepy

def init_api_v1(consumer_key, consumer_secret, access_token, access_token_secret):
    '''
    '''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True)

def init_api_v2():
    '''
    '''
    pass

