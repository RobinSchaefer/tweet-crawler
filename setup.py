import io
from setuptools import find_packages, setup

with io.open('requirements.txt') as f_in:
    install_requires = f_in.read()

setup(
    name='tweet-crawler',
    version='0.0.1',
    author='Robin Schaefer',
    author_email='robin.schaefer@uni-potsdam.de',
    description='A tool for crawling tweets using Tweepy.',
    long_description=io.open('README.md', mode='r', encoding='utf-8').read(),
    keywords='twitter api crawling',
    license='mit',
#    namespace_packages=
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'crawl-tweets-by-ids=tweet_crawler.cli:crawl_tweets_by_ids',
            'crawl-tweets-by-keyword=tweet_crawler.cli:crawl_tweets_by_keyword',
            'stream-tweets-by_keyword=tweet_crawler.cli:stream_tweets_by_keyword'
        ]
    }
)
