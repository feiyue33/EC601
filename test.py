import twitter_api

consumer_key = 'WM7Ps3GT1ifRqfHHfBtpzUIqY'
consumer_secret = 'P0p7twqnbwELXA7czf6YtIjfTHgvSAfDYcKF0sXBqQ6XSGkP4K'
access_key = '1038602494073597952-i3TOPIt196yU44tIgRYmrw66AWwzcQ'
access_secret = 's0RyUZ5hSaq671MNx9dOaXzwv35Lvu1CAWDg3uHJgBTpM'

api = twitter_api.twitter_api()
api.set_consumer_key(consumer_key, consumer_secret)
api.set_access_key(access_key, access_secret)

# connect to twitter
api.get_auth()

img_list = api.get_images('lanadelrey', 20)
api.get_label(img_list)

keyword = 'black'
results = api.mysql_search(keyword)
print('MySQL: These twitter account owns keyword {}'.format(keyword))
for rlt in results:
    print(rlt)

log_num = api.mysql_summary()
print('There are', log_num[0], 'logs in MySQL.')

