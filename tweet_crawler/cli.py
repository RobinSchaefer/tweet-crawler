import click
import io
import json
import tweepy

from .api import init_api

@click.command()
@click.argument('credential-dir', type=click.Path(exists=True))
@click.argument('out-dir', type=click.Path(exists=False))
@click.option('--keyword', help='')
def crawl_tweets_by_keyword(out_dir, credential_dir, keyword):
    '''

    '''

    with io.open(credential_dir) as f_in:
        credentials = json.load(f_in)


    api = init_api(credentials['consumer_key'],
                   credentials['consumer_secret'], 
                   credentials['access_token'], 
                   credentials['access_token_secret'])

    limit = None

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

    with io.open(out_dir, mode='w') as f_out:
        json.dump(tweets, f_out)




@click.command()
@click.argument('credential-dir', type=click.Path(exists=True))
@click.argument('id-dir', type=click.Path(exists=True))
@click.argument('out-dir', type=click.Path(exists=False))
def crawl_tweets_by_ids(credential_dir, id_dir, out_dir):
    '''

    '''

    with io.open(credential_dir) as f_in:
        credentials = json.load(f_in)

    api = init_api(credentials['consumer_key'],
                   credentials['consumer_secret'], 
                   credentials['access_token'], 
                   credentials['access_token_secret']) 

    with io.open(id_dir, mode='r') as f_in:
        ids = f_in.readlines()
        ids = [id_.strip() for id_ in ids]

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

    with io.open(out_dir, mode='w') as f_out:
        json.dump(tweets, f_out)
