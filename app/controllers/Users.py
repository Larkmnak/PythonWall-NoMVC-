from system.core.controller import *
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        print 'Note that we have to load the model before using it in the methods below'
        self.load_model('User')
        self.load_model('Wall_m')
    
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        #'messages = self.models['WelcomeModel'].grab_messages()'
        #'user = self.models['WelcomeModel'].get_user()'
        #'to pass information on to a view it's the same as it was with Flask'
        
        #'return self.load_view('index.html', messages=messages, user=user)'
        """
        return self.load_view('/Login/index.html')

    def login(self):
        print "login function activated"
        user_info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        login_status = self.models['User'].login_user(user_info)
        print 'login status:'
        print login_status
        if login_status['status'] == True:
            print 'loging in'
            # print str(login_status['user']['id'])
            # print str(login_status['user']['first_name'])
            # print str(login_status['user']['last_name'])
            session['user_id'] = login_status['user']['id'] 
            session['first_name'] = login_status['user']['first_name']
            session['last_name'] = login_status['user']['last_name']
            return redirect('/wall')
        else:
            message = 'Incorrect password/email combination'
            flash(message)
            return self.load_view('/Login/index.html')



        # while(ErrorBool == 0):
        #     if not user:
        #         print 'email error'
        #         message = 'Error 86-5 EMAIL NOT FOUND: incorrect email'
        #         ErrorBool = 1
        #         break
        #     else:
        #         print "email equal"
        #         print user[0]['email']
        #     user_query = "SELECT password FROM users WHERE email = :email LIMIT 1"
        #     query_data = { 'email': email }
        #     print password
        #     user = mysql.query_db(user_query, query_data)
        #     print user
        #     if not user:
        #         print 'password error'
        #         message = 'Error 86-5 EMAIL NOT FOUND: incorrect password'
        #         ErrorBool = 1
        #         break
        #     if bcrypt.check_password_hash(user[0]['password'], password):
        #         print 'correct'
        #         print user[0]['password']
        #         user_query = "SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users WHERE email = :email LIMIT 1"
        #         query_data = { 'email': email }
        #         name = mysql.query_db(user_query, query_data)
        #         ErrorBool = 2
        #         break
        #     else:
        #         print 'incorrect'
        #         message = 'Error 86-5 EMAIL NOT FOUND: incorrect password'
        #         ErrorBool = 1
        #         break

        # if ErrorBool == 1:
        #     flash(message)
        #     return redirect('/')
        # else:
        #     flash(name[0]['full_name'])
        #     return redirect('success.html')

    def new(self):
        return self.load_view('/Login/new.html')

    print 'method to create a user'
    def create(self):
        print 'gather data posted to our create method and format it to pass it to the model'
        user_info = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "pw_confirmation" : request.form['pw_confirmation']
        }
        print 'call create_user method from model and write some logic based on the returned value'
        print 'notice how we passed the user_info to our model method'
        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            print 'the user should have been created in the model'
            print 'we can set the newly-created users id and name to session'
            session['user_id'] = create_status['user']['id'] 
            session['first_name'] = create_status['user']['first_name']
            session['last_name'] = create_status['user']['last_name']
            session['email'] = create_status['user']['email']
            print 'we can redirect to the users profile page here'
            return redirect('/wall')
        else:
            print 'set flashed error messages here from the error messages we returned from the Model'
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            print 'redirect to the method that renders the form'
            return self.load_view('/Login/new.html')
