from lda import return_response




chatHistory={}
@app.route('/AskReddit', methods=['GET', 'POST'])
def askReddit():
	return render_template('MemeNews_askReddit.html', chatHistory=chatHistory)
@app.route('/ChatReddit', methods=['GET', 'POST'])
def chatReddit():	
	if request.method== 'GET':
		return redirect('/AskReddit')
	userInput=request.form['userInput']
	output="Huh, you don't want to talk!?"
	if userInput:
		output=return_response(userInput)
		chatHistory[userInput]=output
	return render_template('MemeNews_askReddit.html',userInput=userInput, output=output,chatHistory=chatHistory)
		
