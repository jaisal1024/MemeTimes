from flask import Flask, Markup, render_template, request, session, url_for, redirect
import pymysql.cursors, datetime
app = Flask(__name__)


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