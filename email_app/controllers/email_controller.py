from email_app import app

from flask import render_template, redirect, request, session

from email_app.models.email_model import Email
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# This is the main route that will redirect to the user registration


@app.route('/')
def index():
    return redirect('/registration')

# This route is to render the html page on the browser


@app.route('/registration')
def user_form():
    return render_template('email.html')

# once the user is on the brower it will show a form to fill out, You need to set the method to post along with the form and make the action in the form  equal to this app.route, than code your logic for validation.


@app.route('/registration/new', methods=['POST'])
def registration():

    # This is bringing in the function from the Email class to validate the name, last name and requesting the form, if not it will redirect back to the registration route and will re-render the page with the error messages
    if not Email.validate_reg(request.form):
        return redirect('/registration')

    # This is bringing in the function valid_email staticmethod from the Email class to validate the email and requesting the form, if not it will redirect back to the registration route and will re-render the page with the error messages
    if not Email.validate_reg(request.form):
        return redirect('/registration')

    # this is the final function where if all is correct as far as filling out the form, it will than save the user to the database and redirect it to the registration/login route which will re-render email.html since we want it to be on the same html and page.

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # assigning pw_hash with the bcrypt and assigning request.form with the password data into it.

    # create a data
    data = {
        'password': pw_hash
    }

    user_id = Email.save_user(data)

    Email.save_user(data)
    session['user_id'] = user_id
    return redirect('/registration')

# the app route that will show the html page


@app.route('/user', methods=["POST"])
def user_page():
    data = {
        "email": request.form['email']
    }

    emails = Email.get_email(data)
    if not emails:
        flash('Invalid Login/Password', "login")
        return redirect('/user')
    if not bcrypt.check_password_hash(emails.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/user')
    return redirect('/user/login')


@app.route('/user/login')
def user_login():
    return render_template("user.html")
