
# YOU NEED TO FIND HOW TO GET THE MESSAGE ID FROM THE EXACT MESSAGE ON THE PAGE INTO THE INSERT STATEMENT
# IMPLIMENT LINKS TO OLD MESSAGES NEXT TIME!!


from flask import Flask, request, render_template, session, Markup, redirect
from mysqlconnection import MySQLConnector
# imports the Bcrypt module
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'wall')
app.secret_key = 'super secret key'
# this will load a page that has 2 forms one for registration and login
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/new_user', methods=['POST'])
def newUser():
	return render_template('create.html')

@app.route('/new_user/create', methods=['POST'])
def create_user():
	session['dialogue'] = ''
	email = request.form['email']
	VarEmail = email
	AtCheck = 0
	ErrorBool = 0
	NewStr = ['']
	ComList = ['.','c','o','m', '']
	AtChar = ['@']
	session['dialogue'] = ''
	while ErrorBool == 0:
	    print 'Checking size'
	    if len(VarEmail) < 8:
	        print len(VarEmail)
	        print 'Too small'
	        session['dialogue'] = 'Error 12-4: EMAIL NOT VALID: too short'
	        ErrorBool = 1
	        break
	    print 'Checking for .com'
	    NewStr = list(NewStr)
	    print type(NewStr)
	    for countCom in range(0,4): 
	        count = len(VarEmail)+countCom-4
	        print VarEmail[count]          
	        NewStr.insert(countCom, VarEmail[count])
	    print NewStr
	    if NewStr != ComList:
	        print VarEmail
	        print 'Missing .com'
	        session['dialogue'] = 'Error 30-8: EMAIL NOT VALID: missing .com'
	        ErrorBool = 1
	        break
	    print 'Checking for at symbol in '
	    print VarEmail
	    print AtChar[0]
	    for countAt in range(0, len(VarEmail)):
	        if VarEmail[countAt] == AtChar[0]:
	            print 'symbol found'
	            AtCheck = 1
	            ErrorBool = 2
	            break
	    if AtCheck != 1:
	        print VarEmail
	        print 'Missing symbol'
	        session['dialogue'] = 'Error 30-9: EMAIL NOT VALID: missing @'
	        ErrorBool = 1
	        break
	    else:
	    	ErrorBool = 2
	    	break
	if ErrorBool == 1:
		print 'error'
		return render_template('create.html', dialogue = session['dialogue'])
	password = request.form['password']
	if len(password) < 8:
		session['dialogue'] = 'Error 39-6 PASSWORD ERROR: password must be at least 8 characters long!'
		return render_template('create.html', dialogue = session['dialogue'])
	c_password = request.form['c_password']
	if password != c_password:
		session['dialogue'] = 'Error 39-2 PASSWORD ERROR: passwords did not match!'
		return render_template('create.html', dialogue = session['dialogue'])
	first_name = request.form['first_name']
	if len(first_name) < 3:
		session['dialogue'] = 'Error39-2 FIRST_NAME ERROR: first_name must be more than 2 characters!'
		return render_template('create.html', dialogue = session['dialogue'])
	last_name = request.form['last_name']
	if len(last_name) < 3:
		session['dialogue'] = 'Error39-2 LAST_NAME ERROR: last_name must be more than 2 characters!'
		return render_template('create.html', dialogue = session['dialogue'])
	password = bcrypt.generate_password_hash(password)
	# run validations and if they are successful we can create the password hash with bcrypt
	# pw_hash = bcrypt.generate_password_hash(password)
	# now we insert the new user into the database
	insert_query = "INSERT INTO users (email, password, first_name, last_name, created_at, updated_at) VALUES (:email, :password, :first_name, :last_name, NOW(), NOW())"
	query_data = { 'email': email, 'password': password, 'first_name':first_name, 'last_name':last_name }
	mysql.query_db(insert_query, query_data)
	# redirect to wall page
	return render_template('index.html')
	# we are going to add functions to create new users and login users

@app.route('/login', methods=['POST'])
def login(): 
	message = ''
	print 'login'
	session['email'] = request.form['email']
	print session['email']
	password = request.form['password']
	print password
	user_query = "SELECT email FROM users WHERE email = :email LIMIT 1"
	query_data = { 'email': session['email'] }
	user = mysql.query_db(user_query, query_data) # user will be returned in a list
	print user
	if not user:
		print 'email error'
		message = 'Error 86-5 EMAIL NOT FOUND: incorrect email'
		return render_template('index.html', dialogue = message)
	else:
		print "email equal"
		print user[0]['email']
	user_query = "SELECT password FROM users WHERE email = :email LIMIT 1"
	query_data = { 'email': session['email'] }
	print password
	user = mysql.query_db(user_query, query_data)
	if not user:
		print 'password error'
		message = 'Error 86-5 EMAIL NOT FOUND: incorrect password'
		return render_template('index.html', dialogue = message)
	if bcrypt.check_password_hash(user[0]['password'], password):
		print 'correct'
		return redirect('/wall')
	else:
		print 'incorrect'
		message = 'Error 86-5 EMAIL NOT FOUND: incorrect password'
		return render_template('index.html', dialogue = message)
		
	return render_template('index.html', dialogue = message)

@app.route('/wall')
def wall():
	view_comm = ''
	mark = ''
	user_query = "SELECT id FROM users WHERE email = :email LIMIT 1"
	query_data = { 'email': session['email'] }
	session['user_id']  = mysql.query_db(user_query, query_data)

	user_query = "SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users WHERE email = :email LIMIT 1"
	query_data = { 'email': session['email'] }
	name = mysql.query_db(user_query, query_data)

	user_query = "SELECT messages.message, messages.id AS id, CONCAT(first_name, ' ', last_name) AS full_name FROM messages JOIN users ON messages.users_id = users.id"
	print 'user id: '
	print session['user_id'][0]['id']
	query_data = { 'user_id': session['user_id'][0]['id'] }
	msg = mysql.query_db(user_query, query_data)
	print "MESSAGE: "+str(msg)

	if msg != []:
		user_query = "SELECT comments.comment, comments.messages_id, CONCAT(first_name, ' ', last_name) AS full_name FROM comments JOIN users ON comments.users_id = users.id"
		query_data = { 'messages_id': msg[0]['id'] }
		session['comm'] = mysql.query_db(user_query, query_data)
	else: 
		session['comm'] = []
	print "COMMENT: "+str(session['comm'])
	return render_template('wall.html', Welcome = name[0]['full_name'], mess = msg, comm = session['comm'])
@app.route('/wall/post', methods=['POST'])
def post():
	new_msg = request.form['new_msg']
	insert_query = "INSERT INTO messages (message, users_id, created_at, updated_at) VALUES (:new_msg, :user_id, NOW(), NOW())"
	query_data = { 'new_msg': new_msg, 'user_id': session['user_id'][0]['id'] }
	mysql.query_db(insert_query, query_data)
	return redirect('/wall')

@app.route('/wall/comment/<message_id>', methods=['POST'])
def comment(message_id):
	print session['user_id']
	print message_id
	print request.form['comm_text']
	comment_text = request.form['comm_text']
	insert_query = "INSERT INTO comments (comment, messages_id, created_at, updated_at, users_id) VALUES (:comment_text, :messages_id, NOW(), NOW(), :user_id)"
	query_data = { 'comment_text': comment_text, 'messages_id': message_id, 'user_id': session['user_id'][0]['id'] }
	mysql.query_db(insert_query, query_data)
	print 'Sql Request ran'
	return redirect('/wall')


app.run(debug=True)


# YOU NEED TO FIND HOW TO GET THE MESSAGE ID FROM THE EXACT MESSAGE ON THE PAGE INTO THE INSERT STATEMENT
# IMPLIMENT LINKS TO OLD MESSAGES NEXT TIME!!