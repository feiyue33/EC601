import os
import io
import sys

import tweepy
import urllib.request
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

import pymysql
import pymongo

from datetime import datetime

cur_dir = os.getcwd()

class twitter_api(object):

    def __init__(self):
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_key = ''
        self.access_secret = ''
        self.error = None

        # MySQL connection
        try:
            self.mysql = pymysql.connect(host='localhost',
                                         user='root',
                                         password='mino930330',
                                         db='Twitter_API',
                                         port=3306)
        except Exception as e:
            print('Error: Cannot connect to MySQL! Please check the configuration.')
            raise e

        # MongoDB connection
        try:
            mongodb = pymongo.MongoClient('mongodb://localhost')
            self.mongo = mongodb['Twitter_API']
        except Exception as e:
            print('Error: Cannot connect to MongoDB! Please check the configuration.')
            raise e

    def set_consumer_key(self, c_key, c_secret):
        self.consumer_key = c_key
        self.consumer_secret = c_secret
        return 0

    def set_access_key(self, a_key, a_secret):
        self.access_key = a_key
        self.access_secret = a_secret
        return 0

    def get_auth(self):
        try:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_key, self.access_secret)
            self.api = tweepy.API(auth)
        except Exception as e:
            self.error = e
            raise e
        finally:
            # write log to database
            self.log('get auth from twitter')

        print('Successfully connect to Twitter API.')
        print('------------------------------------')

    def get_images(self, username, img_num):
        log_str = 'download {num} twitter images from @{name}'.format(num=img_num, name=username)
        print('Try to', log_str)

        try:
            usr_tweets = self.api.user_timeline(screen_name=username,
                                                count=img_num, include_rts=False,
                                                exclude_replies=True)
            # output = []
            output_fmt = []
            output_url = []
            output = {}
            img_id = 0
            for tweet in usr_tweets:
                if len(tweet.entities.get('media', [])) > 0:
                    url_str = tweet.entities['media'][0]['media_url']
                    fmt_str = '{name}_{id}.jpg'.format(name=username, id=img_id)
                    urllib.request.urlretrieve(url_str, fmt_str)

                    output_fmt.append(fmt_str)
                    output_url.append(url_str)
                    output = dict(zip(output_fmt, output_url))

                    img_id = img_id + 1
        except Exception as e:
            self.error = e
            raise e
        finally:
            self.log(log_str)

        print('Finish: downloading images!')
        print('------------------------------------')

        return output

    def img2video(self, username):
        command0 = ('ffmpeg -r 0.5 -i {img}_%d.jpg '
                    '-vf scale=-600:600 -y -r 30 '
                    '-t 60 movie.mp4'.format(img=username))

        if os.path.exists('{img}_0.jpg'.format(img=username)):
            os.popen(command0)
        else:
            # write log to database
            self.log('Fail: img2video')
            raise Exception('No image file found in twiiter.')

        self.log('Success: img2video')

    def get_label(self, file_list):
        list_len = len(file_list)

        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        try:
            for file, url in file_list.items():
                description = twitter_api.get_label_from_client(client, file, 5)
                twitter_api.label_image(file, description)
                print(description, url)

                # record into database
                index = file.rfind('_')
                username = file[:index]
                description = description.strip().split('\n')
                print(description)
                self.mongo_label(username, description, url)

                for label in description:
                    self.mysql_label(username, label, url)
                    # self.mongo(username, label)

                print('Progress: ', file, '/', list_len)
            print('Finish: add labels!')
        except Exception as e:
            self.error = e
            print(e)
        finally:
            # print('get label of {} images'.format(list_len))
            self.log('get label of {} images'.format(list_len))

    @staticmethod
    def get_label_from_client(client, img_name, max_label):
        # Loads the image into memory
        with io.open(img_name, 'rb') as image:
            request = { 'image': {'content': image.read()},
                        'features': [
                            {
                            'type': 'LABEL_DETECTION',
                            'max_results': max_label,
                            }
                        ],
            }
        try:
            # Performs label detection on the image file
            response = client.annotate_image(request)
            labels = response.label_annotations
        except Exception as e:
            raise e

        description = ''
        for label in labels:
            # print(label.description)
            description += str(label.description) + '\n'

        return description

    @staticmethod
    def label_image(img_name, label):
        img = Image.open(img_name)
        (w, h) = img.size
        draw = ImageDraw.Draw(img)
        draw.text((w/2-100, h/2-100), label, fill="#ffffff", align='center')
        img.save(img_name)

    def log(self, log_str='Unknown'):
        self.mysql_log(log_str)
        self.mongo_log(log_str)

    def mysql_log(self, log_str='Unknown'):
        if self.error:
            log_str = str(self.error)
        try:
            with self.mysql.cursor() as cursor:
                cursor.execute('INSERT INTO api_log(time, action) VALUES (%s, %s)', (datetime.now(), log_str))
            self. mysql.commit()
        except Exception as e:
            self.mysql.rollback()
            self.mysql.close()
            raise e

    def mysql_label(self, username, label, url):
        try:
            with self.mysql.cursor() as cursor:
                cursor.execute('INSERT INTO img_info(twitter_id, label, time, img_url) VALUES (%s, %s, %s, %s)',
                               (username, label, datetime.now(), url))
        except Exception as e:
            self.error = e
            # self.mysql_log()
            self.mysql.close()
            raise e

    def mysql_search(self, key):
        try:
            with self.mysql.cursor() as cursor:
                cursor.execute('SELECT * FROM img_info WHERE label like "%{}%"'.format(key))
                results = cursor.fetchall()
        except Exception as e:
            self.error = e
            self.mysql.close()
            raise e
        finally:
            self.log('Search {} in MySQL.'.format(key))
        user_list = []
        for row in results:
            if not row[1] in user_list:
                user_list.append(row[1])
        return user_list

    def mysql_summary(self):
        try:
            with self.mysql.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM api_log')
                result = cursor.fetchone()
        except Exception as e:
            self.error = e
            self.mysql.close()
            raise e
        finally:
            self.mysql_log('Count logs in MySQL.')
        return result

    def mongo_log(self, log_str='Unknown'):
        if self.error:
            log_str = str(self.error)
        doc = {
            'time': datetime.now(),
            'action': log_str,
        }
        try:
            api_log = self.mongo['api_log']
            api_log.insert_one(doc)
        except Exception as e:
            print('Fail: Write log to MongoDB.')
            raise e

    def mongo_label(self, username, description, url):
        doc = {
            'twitter_id': username,
            'labels': description,
            'url': url,
        }
        try:
            img_info = self.mongo['img_info']
            img_info.insert_one(doc)
            # cursor = img_info.find({'user_id': username})
        except Exception as e:
            self.error = e
            # self.mongo_log()
            raise e

    def mongo_summary(self):
        try:
            api_log = self.mongo['api_log']
            count = 0
            for i in api_log.find():
                count = count + 1
            return count
        except Exception as e:
            self.error = e
            raise e
        finally:
            self.mongo_log('Count logs in MongoDB.')

    def mongo_search(self, key):
        result = []
        try:
            img_info = self.mongo['img_info']
            for col in img_info.find():
                if key in col['labels']:
                    if col['twitter_id'] in result:
                        continue
                    else:
                        result.append(col['twitter_id'])
            return  result
        except Exception as e:
            self.error = e
            raise e
        finally:
            self.log('Search {} in MySQL.'.format(key))







