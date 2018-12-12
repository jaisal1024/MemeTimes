#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Markup, render_template, request, session, url_for, redirect
from flask_bootstrap import Bootstrap
from lda import return_response
import pandas as pd
import re
import pymysql.cursors
from sqlalchemy import create_engine
import json
import os
from datetime import datetime

app = Flask(__name__)

today = datetime.now().strftime("%A, %B %d, %Y")

#AUTH 
with open('config.json') as f:
    data = json.load(f)
reddit_cred = data['Reddit']
watson_cred = data['Watson']
newspaper_cred = data['News']
img_cred = data["img"]


engine = create_engine("mysql://root:yankees7&@35.237.95.123:3306/MemeNews")

#grab the memes & the associated article
query = '''SELECT * FROM MemeNews.Memes'''
df = pd.read_sql('''SELECT * FROM MemeNews.every_comment''', engine)
df_memes_ = pd.read_sql(query, engine)
df_dict = {}
for index, row in df_memes_.iterrows():
    if (index %2 ==0): 
        query = '''SELECT * FROM MemeNews.Daily_Articles WHERE id LIKE '{0}' LIMIT 1'''.format(row['post_id'])
        df_article = pd.read_sql(query, engine)
        df_dict = df_article.iloc[0].to_dict()
# df_dict['title'], df_dict['url'], df_dict['image'], df_dict['body']

@app.route('/', methods=['GET', "POST"])
def home():
    def create_timeline(df):
        df['created'] = pd.to_datetime(df['created'], unit='s')
        grouped = df.groupby(df.created.dt.date).count()
        grouped.set_index('created')

        a = pd.Series(grouped.post_id)
        a.index = grouped.index
        a.plot()
        timeline = plt.savefig('Timeline')
    
        con = engine.connect()
        con.close()

        return render_template("MemeNews.htm", date = today, 
                               article_title_1 = df_dict['title'],
                               image_url_1 = df_dict['image'],
                               article_entities_1 = df_dict['keywords'],
                               article_url_1 = df_dict['url'],
                               article_summary_1 = df_dict['summary'],
                               timeline = timeline)

@app.route('/Article')
def MemeNews_article():
    return render_template("MemeNews_article.html", date = today)

@app.route('/PastArticles')
def MemeNews_pa():
    con = engine.connect()
    articles = con.execute("SELECT DISTINCT title, summary, url FROM MemeNews.every_article")
    con.close()
    return render_template("MemeNews_pa.html", every_article = articles, date = today)

@app.route('/TheWorldInMemes')
def MemeNews_twim():
    return render_template("MemeNews_twim.html", date = today)

@app.route('/MemeAnalysis_Articles')
def MemeNews_ma_articles():
    return render_template("MemeNews_ma_articles.html", date = today)

@app.route('/MemeAnalysis_Comments')
def MemeNews_ma_comments():
    return render_template("MemeNews_ma_comments.html", date = today)

@app.route('/AboutUs')
def MemeNews_au():
    return render_template("MemeNews_au.html", date = today)

chatHistory={}
@app.route('/AskReddit', methods=['GET', 'POST'])
def askReddit():
	return render_template('MemeNews_askReddit.html', chatHistory=chatHistory, date = today)

@app.route('/ChatReddit', methods=['GET', 'POST'])
def chatReddit():	
	if request.method== 'GET':
		return redirect('/AskReddit')
	userInput=request.form['userInput']
	output="Huh, you don't want to talk!?"
	if userInput:
		output=return_response(userInput)
		chatHistory[userInput]=output
	return render_template('MemeNews_askReddit.html',userInput=userInput, output=output,chatHistory=chatHistory, date = today)
		

@app.route('/Subscribe')
def MemeNews_subscribe():
    return render_template("MemeNews_subscribe.html", date = today)

@app.route('/TermsOfService')
def MemeNews_tos():
    return render_template("MemeNews_tos.html", date = today)

@app.route('/SiteMap')
def MemeNews_sm():
    return render_template("MemeNews_sm.html", date = today)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
