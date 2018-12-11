from flask import Flask, Markup, render_template, request, session, url_for, redirect
import pymysql.cursors, datetime
from sqlalchemy import create_engine
import pandas as pd
app = Flask(__name__)

#AUTH 
with open('config.json') as f:
    data = json.load(f)
reddit_cred = data['Reddit']
watson_cred = data['Watson']
newspaper_cred = data['News']
sql_cred = data["SQL"]
img_cred = data["img"]

#SQL
conn_string = 'mysql://{user}:{password}@{host}/{db}?charset=utf8mb4'.format(
    host = sql_cred["host"], 
    user = sql_cred["user"],
    password = sql_cred["password"], 
    db = 'MemeNews')
engine = create_engine(conn_string)

#grab the memes & the associated article
query = '''SELECT * FROM MemeNews.Memes'''
df_memes_ = pd.read_sql(query, engine)
for index, row in df_memes_.iterrows():
    if (index %2 ==0): 
        query = '''SELECT * FROM MemeNews.Daily_Articles WHERE id LIKE '{0}' LIMIT 1'''.format(row['post_id'])
        df_article = pd.read_sql(query, engine)
        print(df_article['title'], df_article['image'], df_article['keywords'], df_article['url'], df_article['summary'])
        

@app.route('/', methods=['GET', "POST"])
def main():
	return render_template('index.html')

@app.route('/articles', methods=['GET', "POST"])
def article():
	return render_template('articles.html')

@app.route('/meme', methods=['GET', "POST"])
def articles():
	return render_template('meme.html')

if __name__ == "__main__":
    app.run(debug=True)