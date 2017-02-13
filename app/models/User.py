from system.core.model import *
import re     # still need to import this module: we use regular expressions to validate email formats!
class User(Model):
    def __init__(self):
        super(User, self).__init__()
    def create_user(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        # OLD REGEX : r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$'
        EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        
        

        errors = []
        # Some basic validation
        if not info['first_name']:
            errors.append('Name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            # Code to insert user goes here...
            hashed_pw = self.bcrypt.generate_password_hash(info['password'])
            get_user_query = "INSERT INTO users (first_name, last_name, email, password) VALUES(:first_name, :last_name, :email, :password)"
            data = { 
                'first_name' : info['first_name'],
                'last_name' : info['last_name'],
                'email' : info['email'],
                'password' : hashed_pw
            }
            users = self.db.query_db(get_user_query, data)
            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        # same as query_db() but returns one result
        user = self.db.get_one(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user.password, password):
                get_user_query = 'SELECT * FROM users WHERE email = :email LIMIT 1'
                user_data = {'email': info['email']}
                user = self.db.query_db(get_user_query, user_data)
                user = user[0]
                print 'user'
                print user
                return { "status": True, "user": user} #add ', "user": user' to trun back
        # Whether we did not find the email, or if the password did not match, either way return False
        return { "status": False }