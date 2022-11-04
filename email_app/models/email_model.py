from email_app.config.mysqlconnection import connectToMySQL
from flask import flash
# importing re for email validation
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Email:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['creadted_at']
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
                flash("You need to enter your first name")
                valid_user = False
            if len(user['last_name']) == 0:
                flash("You need to end your last name")
                valid_user = False
            return valid_user

        # staticmethod for email validation
    @staticmethod
    def valid_email(email):
            # setting a var to true to be returned if email matched REGEX
            is_valid = True
            if not EMAIL_REGEX.match(email['email']):
                flash("Invalid email address!")
                is_valid = False
            return is_valid
