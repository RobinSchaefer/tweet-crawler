# Tweet Crawler

This repo contains code for crawling tweets using the [Tweepy](https://www.tweepy.org/) 
library. Tweets can be crawled using a keyword or tweet IDs. You need to 
register with the [Twitter Developer Platform](https://developer.twitter.com/en)
to get your credentials. These are needed to access the Twitter API.

## Installation

Clone the repo to your machine and use pip to install it.

```
pip install .
```

## Usage

Tweets can be crawled using
- keyword (`crawl-tweets-by-keyword`)
- IDs (`crawl-tweets-by-ids`)

For usage information please refer to the documentation. 

```
crawl-tweets-by-keyword --help
Usage: crawl-tweets-by-keyword [OPTIONS] CREDENTIAL_DIR OUT_DIR

  Crawl tweets by keyword.

  Arguments: 
  credential-dir  The directory of the credential json file.
  out-dir The output directory where crawled tweets will be stored.

Options:
  --keyword TEXT  The tweet keyword.
  --help          Show this message and exit.
```

```
crawl-tweets-by-ids --help
Usage: crawl-tweets-by-ids [OPTIONS] CREDENTIAL_DIR ID_DIR OUT_DIR

  Crawl tweets by ids.

  Arguments: 
  credential-dir  The directory of the credential json file.
  id-dir  The directory of the id txt file.
  out-dir The output directory where crawled tweets will be stored.

Options:
  --help  Show this message and exit.
```
## License

MIT
