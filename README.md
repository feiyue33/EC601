# EC601 - MiniProject1 & MiniProject3
Mini Project 1 and Mini Project 3 of EC601 class from Boston University.

## Introduction

### Mini Project 1
This API uses Tweepy to download images from a Twitter account，uses GoogleVision to label images and finally uses ffmpeg to make images to a video.
These python files belong to Mini Project 1:
* test_tweepy.py
* rename.py
* vision.py
* main.py
Run main.py to use the API. The images downloaded from Twitter account will store on your PC. The output video is test.avi.

### Mini Project 3
Use database to store image information and log. Both SQL(MySQL) and NoSQL(MongoDB) are implemented. In mini project 3, the functions and files are reorganzied and fine-tuned. Also, more exceptions are considered.
These python files belong to Mini Project 3:
* twitter_api.py
* test.py
Run test.py to use the API. The images downloaded from Twitter account will store on your PC. The output video is test.avi. Logs and image information are stored in database.

## Requirements

### Packages
In order to successfully use the API, these packages should be installed first:

* Tweepy
```
pip install tweepy
```

* wget
```
pip install wget
```

* FFmpeg

You can download FFmpeg from official website: http://ffmpeg.org/

* GoogleVision
```
pip install google-cloud-vision
```

* PyMySQL
```
pip install pymysql
```

* PyMongo
```
pip install pymongo
```

### Database
Please make sure MySQL and MongoDB are successfully installed on your PC.

* MySQL:
https://www.mysql.com/downloads/

* MongoDB:
https://www.mongodb.com/

## Quick Start

### Create A New Database in MySQL
```SQL
CREATE DATABASE Twitter_API;
```














