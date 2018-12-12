import re
from datetime import timedelta, datetime, date
import time
import requests
import requests.auth
import pandas as pd
from newspaper import Article
import praw
from praw.models import MoreComments
import json
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR

with open('config.json') as f:
    data = json.load(f)
reddit_cred = data['Reddit']
watson_cred = data['Watson']
newspaper_cred = data['News']
sql_cred = data["SQL"]
img_cred = data["img"]

#Authentification
reddit = praw.Reddit(**reddit_cred)

#Connect to Database
conn_string = 'mysql://{user}:{password}@{host}/{db}?charset=utf8mb4'.format(
    host = sql_cred["host"],
    user = sql_cred["user"],
    password = sql_cred["password"],
    db = 'MemeNews')
engine = create_engine(conn_string)

query = '''SELECT id FROM MemeNews.Daily_Articles WHERE created > 1544567401.703595 ORDER BY score DESC LIMIT 10'''
article_ids = engine.execute(query)
article_list = [value for value, in article_ids]
for post_id in article_list:
    query_comments = '''SELECT EXISTS(SELECT * FROM MemeNews.every_comment WHERE post_id LIKE '{0}' LIMIT 1)'''.format(post_id)
    exists = engine.execute(query_comments)
    for item in exists:
        print(item)
    if (exists):
        print("comments exists article: ", post_id)
