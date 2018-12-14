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
from sqlalchemy.orm import sessionmaker
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

yest = (datetime.utcnow()-timedelta(hours = 24)).timestamp()

#query = '''SELECT id FROM MemeNews.Daily_Articles WHERE created > {0} ORDER BY score DESC'''.format(yest)
query = '''SELECT id FROM MemeNews.Daily_Articles ORDER BY score DESC'''
article_ids = engine.execute(query)
article_list = [value for value, in article_ids]
for post_id in article_list:
    query_comments = '''SELECT EXISTS(SELECT * FROM MemeNews.every_comment WHERE post_id LIKE '{0}' LIMIT 1)'''.format(post_id)
    if (not engine.execute(query_comments).fetchone()[0]):
        submission = reddit.submission(post_id)
        comment_dict = {
            "post_id":[],
            'post_title':[],
            "id": [],
            "author":[],
            "body":[],
            "created": [],
            'score':[],
            'is_submitter':[],
            'parent_id':[]}
        for top_level_comment in submission.comments.list()[:100]:
            try:
                comment_dict['is_submitter'].append(top_level_comment.is_submitter)
                comment_dict['post_id'].append(submission.id)
                comment_dict['id'].append(top_level_comment.id)
                comment_dict['author'].append(top_level_comment.author)
                comment_dict['body'].append(re.sub(r'[^\x00-\x7F]', '', top_level_comment.body))
                comment_dict['score'].append(top_level_comment.score)
                comment_dict['created'].append(top_level_comment.created_utc)
                comment_dict['parent_id'].append(top_level_comment.parent_id)
                comment_dict['post_title'].append(submission.title)
            except:
                continue
        comment_data = pd.DataFrame(comment_dict)
        comment_data.to_sql('every_comment', con = engine, if_exists='append', dtype={'None':VARCHAR(5)})
        print("comments added")
