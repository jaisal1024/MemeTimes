#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Markup, render_template, request, session, url_for, redirect
from flask_bootstrap import Bootstrap
from lda import return_response
import pandas as pd
from bokeh.io import save
import re
from sqlalchemy import create_engine
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
app = Flask(__name__)
from make_plot_for import generate_lda_for
today = datetime.now().strftime("%A, %B %d, %Y")
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar

#AUTH
with open('config.json') as f:
    data = json.load(f)
reddit_cred = data['Reddit']
watson_cred = data['Watson']
newspaper_cred = data['News']
# img_cred = data["img"]

engine = create_engine("mysql://root:yankees7&@35.237.95.123:3306/MemeNews")

#grab the memes & the associated article
articles_list = []
query = '''SELECT * FROM MemeNews.Memes ORDER BY post_id LIMIT 10'''
df = pd.read_sql('''SELECT * FROM MemeNews.every_comment''', engine)
df['created'] = pd.to_datetime(df['created'], unit='s')
df_memes_ = pd.read_sql(query, engine)
memes = [None]*2
i = 0
for index, row in df_memes_.iterrows():
    if (index % 2 == 1):
        query = '''SELECT * FROM MemeNews.Daily_Articles WHERE id LIKE '{0}' LIMIT 1'''.format(row['post_id'])
        df_article = pd.read_sql(query, engine)
        df_dict = df_article.iloc[0].to_dict()
        memes[1] = row["meme_url"]
        memes_copy = memes[:]
        df_dict["meme_urls"] = memes_copy
        articles_list.append(df_dict)
        df_dict = {}
    else:
        memes[0] = row["meme_url"]

def create_timeline(df):

    df['created'] = pd.to_datetime(df['created'], unit='s')
    grouped = df.groupby(df.created.dt.date).count()
    grouped.set_index('created')

    a = pd.Series(grouped.post_id)
    a.index = grouped.index

    # a.plot()
    # plt.savefig('Timeline')
    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom,tap"
    p = figure(plot_height=350,
    title="Daily number of comments",
    tools=TOOLS,
    toolbar_location='above')
    # print(a.columns)

    p.vbar(x=a.index, top=a.values, width=2)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.xaxis.axis_label = 'Day'
    p.yaxis.axis_label = 'Comments'
    p.select_one(HoverTool).tooltips = [
        ('month', '@x'),
        ('Number of comments', '@top'),
    ]
    output_file("barchart.html", title="barchart")
    save(p)
create_timeline(df)
print(articles_list[0]["meme_urls"], articles_list[4]["meme_urls"])

for i in range(len(articles_list)):
    post_id = articles_list[i]['id']
    df_article = df[df['post_id']==post_id]
    if df_article.shape[0] <= 5000:
        continue
    else:
        plot_name = generate_lda_for(df_article, 'article'+str(post_id), 15)
        print(plot_name)
        articles_list[i]['plot'] = plot_name
    # print(articles_list[i].keys())

@app.route('/', methods=['GET', "POST"])
def home():
#     def create_timeline(df):
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
                           articles_list=articles_list,
                           timeline = timeline)

@app.route('/Article')
def MemeNews_article():
    return render_template("MemeNews_article.html", date = today)

@app.route('/PastArticles')
def MemeNews_pa():
    con = engine.connect()
    articles = con.execute("SELECT DISTINCT title, summary, url FROM MemeNews.Daily_Articles")
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


@app.route('/Subscribe', methods=["GET", "POST"])
def MemeNews_subscribe():
    if request.method=='GET':
        return render_template("MemeNews_subscribe.html", date = today)
    elif request.method=='POST':
        return render_template("MemeNews_subscribe.html", date= today, thanks='Thank you for subscribing to MemeTimes newsletter!')



@app.route('/TermsOfService')
def MemeNews_tos():
    return render_template("MemeNews_tos.html", date = today)

@app.route('/SiteMap')
def MemeNews_sm():
    return render_template("MemeNews_sm.html", date = today)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
