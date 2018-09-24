#!/usr/bin/env python

import test_tweepy
import rename
# import make_video
import vision
import os

test_tweepy.get_twitter_images('lanadelrey')
print("Successfully get images from Twitter!")
rename.rename()
vision.label_images()
mkv_cmd = 'ffmpeg -r 1 -i pic%d.jpg -vcodec mpeg4 test.avi'
# read_make_video = make_video.read()
mkv_cmd_exe = os.popen(mkv_cmd, 'r', 1)
print("Successfully make the video!")
