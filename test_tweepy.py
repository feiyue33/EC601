import tweepy
from tweepy import OAuthHandler
import json
import wget

consumer_key = 'jJsxpMjxxoD8DvmWW0uWwT428'
consumer_secret = 'W2bm9Zw6QyfGoclzChKFaup2PWUhNP9ETa4bGZ9aURI0P0M42a'
access_token = '1038602494073597952-Xu2fJkM4JWNMlD80uGyaOy8zEaxKum'
access_secret = 'VTKaGPVjP76rbLBmPjI8nlAqmi6gjYdkkcTcBfEiI0Tjp'

# refer to https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/

# @classmethod
# def parse(cls, api, raw):
#     status = cls.first_parse(api, raw)
#     setattr(status, 'json', json.dumps(raw))
#     return status


# Status() is the data model for a tweet
# tweepy.models.Status.first_parse = tweepy.models.Status.parse
# tweepy.models.Status.parse = parse

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def get_twitter_images(username):
    usr_tweets = api.user_timeline(screen_name=username,
                                   count=200, include_rts=False,
                                   exclude_replies=True)

    last_id = usr_tweets[-1].id
    while True:
        more_tweets = api.user_timeline(screen_name=username,
                                        count=200,
                                        include_rts=False,
                                        exclude_replies=True,
                                        max_id=last_id - 1)

    # no more tweets
        if len(more_tweets) == 0:
            break
        else:
            last_id = more_tweets[-1].id - 1
            usr_tweets = usr_tweets + more_tweets

    media_files = set()
    for status in usr_tweets:
        media = status.entities.get('media', [])
        if len(media) > 0:
            media_files.add(media[0]['media_url'])

    # download images
    for media_file in media_files:
        wget.download(media_file)
