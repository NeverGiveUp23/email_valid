from email_app.config.mysqlconnection import connectToMySQL
from flask import flash
# importing re for email validation
import re


EMAIL_REGEX = re.compile(
    '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$')


class Email:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # Class for the user input to be saved in the registration form
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO register (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        # setting result to equal the connection between SQL
        results = connectToMySQL('email').query_db(query, data)

        return results

        # Static method to validate the registration form
    @staticmethod
    def validate_reg(user):
        valid_user = True
        if len(user['first_name']) == 0:
            flash("You need to enter your first name", "register")
            valid_user = False
        if len(user['last_name']) == 0:
            flash("You need to enter your last name",  "register")
            valid_user = False
        valid_user = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!",  "register")
            valid_user = False
        return valid_user

    @classmethod
    def get_email(cls, data):
        #
        query = 'SELECT * FROM register WHERE email = %(email)s;'
        result = connectToMySQL('email').query_db(query, data)
        #
        if len(result) < 1:
            return False
        return cls(result[0])
