from flask import Flask, Markup, render_template, request, session, url_for, redirect
import pymysql.cursors, datetime
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
	userInput=request.args.getlist('userInput');
	return render_template('askReddit.html',userInput=userInput)




if __name__ == "__main__":
    app.run(debug=True)