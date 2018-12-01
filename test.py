import twitter_api

consumer_key = 'Your consumer key'
consumer_secret = 'Your consumer secrets'
access_key = 'Your access key'
access_secret = 'Your access secrets'

twitter_account = 'lanadelrey'
img_num = 20

api = twitter_api.twitter_api()

# set keys and secrets of twitter api
api.set_consumer_key(consumer_key, consumer_secret)
api.set_access_key(access_key, access_secret)

# connect to twitter
api.get_auth()

img_list = api.get_images(twitter_account, img_num)
api.get_label(img_list)

keyword = 'black'

mysql_user_results = api.mysql_search_user(keyword)
print('MySQL: These twitter account have keyword {}'.format(keyword))
for rlt in mysql_user_results:
    print(rlt)

mongo_user_results = api.mongo_search_user(keyword)
print('MongoDB: These twitter account have keyword {}'.format(keyword))
for rlt in mongo_user_results:
    print(rlt)

mysql_img_results = api.mysql_search_img(keyword)
print('MySQL: These images contain label {}'.format(keyword))
for rlt in mysql_img_results:
    print(rlt)

mongo_img_results = api.mongo_search_img(keyword)
print('MongoDB: These images contain label {}'.format(keyword))
for rlt in mongo_img_results:
    print(rlt)

log_mysql_num = api.mysql_summary()
print('There are', log_mysql_num[0], 'logs in MySQL.')

log_mongo_num = api.mongo_summary()
print('There are', log_mongo_num, 'logs in MongoDB.')

api.img2video('lanadelrey')

