#!/usr/bin/env python

import os
import sys

mkv_cmd = 'ffmpeg -r 1 -i pic%d.jpg -vcodec mpeg4 test.avi'

# read_make_video = make_video.read()

mkv_cmd_exe = os.popen(mkv_cmd, 'r', 1)