""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Wall_m(Model):
    def __init__(self):
        super(Wall_m, self).__init__()

    def full_name(self, info):
        print info
        user_query = "SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users WHERE id = :id LIMIT 1"
        query_data = { 'id': info }
        name = self.db.query_db(user_query, query_data)
        return name

    def load_messages(self, info):
        print info
        user_query = "SELECT messages.message, messages.id AS id, CONCAT(first_name, ' ', last_name) AS full_name FROM messages JOIN users ON messages.users_id = users.id"
        query_data = { 'user_id': info }
        msg = self.db.query_db(user_query, query_data)
        return msg

    def load_comments(self, info):
        print "info:"
        print info
        user_query = "SELECT comments.comment, comments.messages_id, CONCAT(first_name, ' ', last_name) AS full_name FROM comments JOIN users ON comments.users_id = users.id"
        query_data = { 'messages_id': info }
        comments = self.db.query_db(user_query, query_data)
        return comments

    def post_message(self, info):
        print 'info:'
        print info
        insert_query = "INSERT INTO messages (message, users_id, created_at, updated_at) VALUES (:new_msg, :user_id, NOW(), NOW())"
        query_data = { 'new_msg': info['new_msg'], 'user_id': info['user_id'] }
        self.db.query_db(insert_query, query_data)

    def post_comment(self, info):
        print 'info:'
        print info
        insert_query = "INSERT INTO comments (comment, messages_id, created_at, updated_at, users_id) VALUES (:comment_text, :messages_id, NOW(), NOW(), :user_id)"
        query_data = { 'comment_text': info['comment'], 'messages_id': info['message_id'], 'user_id': info['user_id'] }
        self.db.query_db(insert_query, query_data)

    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """