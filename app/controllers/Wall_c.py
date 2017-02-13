from system.core.controller import *
print 'Starting Wall_c controller'
class Wall_c(Controller):
    def __init__(self, action):
        super(Wall_c, self).__init__(action)
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
        print "Starting Wall"
        print "Retrieving name"
        print session['user_id']
        full_name = self.models['Wall_m'].full_name(session['user_id']) # Grab user'sname
        print full_name
        full_name = full_name[0]['full_name']
        print full_name 

        messages = self.models['Wall_m'].load_messages(session['user_id'])
        print "MESSAGE: "+str(messages)

        if messages != []:
            comments = self.models['Wall_m'].load_comments(messages)
        else: 
            comments = []

        print "COMMENT: "+str(comments)
        return self.load_view('wall.html', Welcome = full_name, mess = messages, comm = comments)

    def message(self):
        print 'post_message starting'
        print request.form['new_msg']
        info = { 'new_msg' : request.form['new_msg'], 'user_id' : session['user_id'] }
        self.models['Wall_m'].post_message(info)
        return redirect('/wall')

    def comment(self, message_id):
        print session['user_id']
        print message_id
        print request.form['comm_text']
        info = { 'comment' : request.form['comm_text'], 'message_id' : message_id, 'user_id' : session['user_id'] }
        self.models['Wall_m'].post_comment(info)
        return redirect('/wall')