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

### Create A New Database

#### Create a new database in MySQL
* Create a new database
```SQL
CREATE DATABASE Twitter_API;
```
* Create new tables

(1) api_log
```SQL
CREATE TABLE api_log(
	log_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	time  DATETIME,
	action VARCHAR(50));
```

(2) img_info
```SQL
CREATE TABLE img_info(
	label_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	twitter_id VARCHAR(50),
	label VARCHAR(50),
	time DATETIME NULL,
	img_url VARCHAR(200));
```

#### Create a new database in MongoDB
You can skip this step because the API will automatically create a new database in MongoDB.

### Set keys and secrets to use Twitter API
You need to provide your own keys and secrets in test.py, line 3 to 6.
```Python
consumer_key = 'Your consumer key'
consumer_secret = 'Your consumer secrets'
access_key = 'Your access key'
access_secret = 'Your access secrets'
```

### Provide Google Vision key file
You need to put your Google Vision key file under the project folder.

### Specify the twitter account
You can specify the twitter account that you want to download images from. Also, you can set the number of images. The test.py default set twitter account to 'lanadelrey' and the number of images to 20.

### Set MySQL database
You should reset MySQL configuration in twitter_api.py, line 27 to 31 to successfully connect to MySQL.
```Python
    self.mysql = pymysql.connect(host='localhost',
				 user='root',
				 password='your password',
				 db='Twitter_API',
				 port=3306)
```

### Search information
You can set the keyword to search information. You can find which twitter accounts or images include keyword label.
