import click
import io
import json
import os
import tweepy

from .api import init_api_v1, init_api_v2
from .config import * 

@click.command()
@click.argument('credential-dir', type=click.Path(exists=True))
@click.argument('out-dir', type=click.Path(exists=False))
@click.option('--keyword', help='The tweet keyword.')
@click.option('--api-version', '-a', default='v2')
def crawl_tweets_by_keyword(out_dir, credential_dir, keyword, api_version):
    '''
    Crawl tweets by keyword. 

    \b
    Arguments: 
    credential-dir  The directory of the credential json file.
    out-dir The output directory where crawled tweets will be stored.

    '''

    with io.open(credential_dir) as f_in:
        credentials = json.load(f_in)

    if api_version == 'v2':
        pass
    elif api_version == 'v1':
        api = init_api_v1(credentials['consumer_key'],
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

            if len(tweets) % 5000 == 0:
                dir_name = os.path.dirname(out_dir)
                file_path = os.path.join(dir_name, 'tweets_' + str(len(tweets)) + '.json')
                with io.open(file_path, mode='w') as f_out:
                    json.dump(tweets,f_out) 

    print('END: Tweet Collection')
    print('\nTotal # of tweets: {}'.format(len(tweets)))

    with io.open(out_dir, mode='w') as f_out:
        json.dump(tweets, f_out)


@click.command()
@click.argument('id-dir', type=click.Path(exists=True))
@click.argument('out-dir', type=click.Path(exists=False))
@click.option('--print-at', '-p', default=1000)
@click.option('--save-at', '-s', default=5000)
@click.option('--api-version', '-a', default='v2')
def crawl_tweets_by_ids(id_dir, out_dir, print_at, save_at, api_version):
    '''
    Crawl tweets by ids. 

    \b
    Arguments: 
    id-dir  The directory of the id txt file.
    out-dir The output directory where crawled tweets will be stored.
    '''

    with io.open(id_dir, mode='r') as f_in:
        ids = f_in.readlines()
        ids = [id_.strip() for id_ in ids]
    
    #no_status_dir = os.path.join(os.path.dirname(out_dir), 'no_status.txt')

    tweets =[]
    #no_status = [] 
    batch_size = 100

    if api_version == 'v2':
        #client = init_api_v2(CONSUMER_KEY,
        #                    CONSUMER_SECRET,
        #                    ACCESS_TOKEN,
        #                    ACCESS_TOKEN_SECRET)

        client = init_api_v2(BEARER_TOKEN)

        tweet_fields = ['attachments', 'author_id',  'context_annotations', 'conversation_id',
                    'created_at', 'entities', 'in_reply_to_user_id', 'lang', 'public_metrics',
                    'referenced_tweets']

        user_fields = ['created_at', 'description', 'location', 'public_metrics']

        media_fields = ['url', 'public_metrics', 'alt_text']

        expansions = ['author_id', 'attachments.media_keys']
        
        print('\nSTART: Tweet Collection')
        print('# of Tweet IDs: {}'.format(len(ids)))

        print_counter = 0
        for i in range(0, len(ids), batch_size):
            ids_batch = ids[0:0+batch_size]

            collected_tweets = client.get_tweets(ids=ids_batch, 
                                            tweet_fields=tweet_fields, 
                                            user_fields=user_fields, 
                                            media_fields=media_fields, 
                                            expansions=expansions)

            for ii in range(batch_size):

                tweet_json = collected_tweets.data[ii].data

                if 'author_id' in expansions:
                    user_id_mapping = {user.data['id']: user.data for user in collected_tweets.includes['users']}
                    
                    tweet_json['user'] = user_id_mapping[tweet_json['author_id']]
                
                if 'attachments.media_keys' in expansions:
                    media_key_mapping = {media.data['media_key']: media.data for media in collected_tweets.includes['media']} 
                    
                    if 'attachments' in tweet_json.keys():
                        tweet_json['media'] = [media_key_mapping[media_key] for media_key in tweet_json['attachments']['media_keys']]
                
                tweets.append(tweet_json)
                
                print_counter+=1
                if print_counter % print_at == 0:
                    print('# of tweets collected: {}'.format(print_counter))
        
                if len(tweets) % save_at == 0:
                    print('# of tweets saved: {}\n'.format(len(tweets)))
                    dir_name = os.path.dirname(out_dir)
                    file_path = os.path.join(dir_name, 'tweets_' + str(len(tweets)) + '.json')
                    with io.open(file_path, mode='w') as f_out:
                        json.dump(tweets,f_out)   
        
    elif api_version == 'v1':
        api = init_api_v1(CONSUMER_KEY,
                        CONSUMER_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET) 

        print('\nSTART: Tweet Collection')
        for i, id_ in enumerate(ids):

            try:
                tweet = api.get_status(int(id_), tweet_mode='extended')
                tweets.append(tweet._json)
            except Exception as e:
                # check if status exists
                if e.args[0][0]['code'] == 144:
                    no_status.append(id_)

                #print(id_)
                #if hasattr(tweet, 'retweeted_status'):
                #    print('{} is a retweet'.format(id_))
                #print('Tweet ID {} could not be selected.'.format(id_))
            if i % print_at == 0:
            
                print('# of tweets: {}'.format(i))
        
            if len(tweets) % save_at == 0:
                dir_name = os.path.dirname(out_dir)
                file_path = os.path.join(dir_name, 'tweets_' + str(len(tweets)) + '.json')
                with io.open(file_path, mode='w') as f_out:
                    json.dump(tweets,f_out)                

    print('END: Tweet Collection')
    print('\nTotal # of tweets: {}'.format(len(tweets)))
    #print('\nTotal # of no status: {}'.format(len(no_status)))

    dir_name = os.path.dirname(out_dir)
    file_path = os.path.join(dir_name, 'tweets_final' + '.json')
    with io.open(file_path, mode='w') as f_out:
        json.dump(tweets, f_out)
    
    #with io.open(no_status_dir, mode='w') as f_out:
    #    for id_ in no_status:
    #        f_out.write(str(id_)+'\n')


@click.command()
@click.argument('credential-dir', type=click.Path(exists=True))
@click.argument('out-dir', type=click.Path(exists=False))
@click.option('--keyword', help='The tweet keyword.')
def stream_tweets_by_keyword(out_dir, credential_dir, keyword):
    '''
    Stream tweets by keyword (using the Twitter streaming API). 

    \b
    Arguments: 
    credential-dir  The directory of the credential json file.
    out-dir The output directory where crawled tweets will be stored.

    '''

    with io.open(credential_dir) as f_in:
        credentials = json.load(f_in)


    api = init_api(credentials['consumer_key'],
                   credentials['consumer_secret'], 
                   credentials['access_token'], 
                   credentials['access_token_secret'])

    limit = None

    tweets =[]

    # check if out-dir already exists; if yes delete it
    if os.path.isfile(out_dir):
        os.remove(out_dir)

    class CustomStreamListener(tweepy.StreamListener):
        def __init__(self):
            super(tweepy.StreamListener, self).__init__()
            self.tweets = []
        
        def on_data(self, data):
            try:
                tweet_data = json.loads(data)
                with io.open(out_dir, mode='a') as f_out:
                    json.dump(tweet_data, f_out)
            except:
                pass
            
    

    print('\nSTART: Tweet Collection')

    listener = CustomStreamListener()
    twitter_stream = tweepy.Stream(auth=api.auth, listener=listener)

    import pdb; pdb.set_trace()

    try:
        twitter_stream.filter(track=[keyword], languages=['de'])
    except KeyboardInterrupt:
        twitter_stream.disconnect()

    import pdb; pdb.set_trace()
    #if limit:
    #    for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='de', tweet_mode='extended').items(limit):
    #        tweets.append(tweet._json)

    #        if len(tweets) % 200 == 0:
    #            print('# of tweets: {}'.format(len(tweets)))
    #else:
    #    for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='de', tweet_mode='extended').items():
    #        tweets.append(tweet._json)

    #        if len(tweets) % 200 == 0:
    #            print('# of tweets: {}'.format(len(tweets)))

    #        if len(tweets) % 5000 == 0:
    #            dir_name = os.path.dirname(out_dir)
    #            file_path = os.path.join(dir_name, 'tweets_' + str(len(tweets)) + '.json')
    #            with io.open(file_path, mode='w') as f_out:
    #                json.dump(tweets,f_out) 

    #print('END: Tweet Collection')
    #print('\nTotal # of tweets: {}'.format(len(tweets)))

    #with io.open(out_dir, mode='w') as f_out:
    #    json.dump(tweets, f_out)