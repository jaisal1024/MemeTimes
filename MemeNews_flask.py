#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Markup, render_template, request, session, url_for, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
import re
import pymysql.cursors
from sqlalchemy import create_engine
import json
import os
from datetime import datetime

app = Flask(__name__)

today = datetime.now().strftime("%A, %B %d, %Y")

@app.route('/')
def home():    
    return render_template("MemeNews.htm", date = today)

@app.route('/Article')
def MemeNews_article():
    return render_template("MemeNews_article.html", date = today)

@app.route('/PastArticles')
def MemeNews_pa():
    engine = create_engine("mysql://root:yankees7&@35.237.95.123:3306/MemeNews")
    con = engine.connect()
    articles = con.execute("SELECT DISTINCT title, summary, url FROM MemeNews.every_article")
    #comments = con.execute("SELECT DISTINCT title, summary, url FROM MemeNews.every_comment")
    con.close()
    return render_template("MemeNews_pa.html", every_article = articles, date = today)

@app.route('/TheWorldInMemes')
def MemeNews_twim():
    return render_template("MemeNews_twim.html", date = today)

@app.route('/AboutUs')
def MemeNews_au():

    return render_template("MemeNews_au.html", date = today)

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
