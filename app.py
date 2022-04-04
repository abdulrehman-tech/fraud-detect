from flask import Flask, render_template, flash, redirect, request, session, logging, url_for

from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegisterForm

from werkzeug.security import generate_password_hash, check_password_hash

from forms import SpamForm
from model import get_result
from file_reader import reader

# Now create flask application object

app = Flask(__name__)

# Database Configuration and Creating object of SQLAlchemy

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vlvdnlnijnabtv:c898b0fe36d87c08f9413b9ad85bcbeacd3b01351d7efed061e15027ad0e9ca8@ec2-44-194-4-127.compute-1.amazonaws.com:5432/dbc8monq512n2c'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create User Model which contains id [Auto Generated], name, username, email and password

class User(db.Model):

    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key=True)

    name= db.Column(db.String(15), unique=True)

    username = db.Column(db.String(15), unique=True)

    email = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(256), unique=True)

@app.route('/', methods = ['GET','POST'])

def home():

    spamform = SpamForm(request.form)
    msg = ""
    


    if request.form.get('btn_reader') == 'reader':
        msg = reader()
        spamform.name.data = msg

    result = ""
    if request.method == 'POST' and spamform.validate:
        
        txt = spamform.name.data
        result = get_result(txt)
        
    return render_template('index.html', form=spamform, message=result)


@app.route('/register/', methods = ['GET', 'POST'])
def register():
    # Creating RegistrationForm class object
    form = RegisterForm(request.form)

    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():

        # if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # create new user model object
        new_user = User(

            name = form.name.data, 


            email = form.email.data, 

            password = hashed_password )

        # saving user object into data base with hashed password
        db.session.add(new_user)

        db.session.commit()

        flash('You have successfully registered', 'success')

        # if registration successful, then redirecting to login Api
        return redirect(url_for('login'))

    else:

        # if method is Get, than render registration form
        return render_template('register.html', form = form)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    # Creating Login form object
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        user = User.query.filter_by(email = form.email.data).first()

        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user.password, form.password.data):
                # if password is matched, allow user to access and save email and username inside the session
                flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user.email 

                session['username'] = user.username
                # After successful login, redirecting to home page
                return redirect(url_for('home'))

            else:

                # if password is in correct , redirect to login page
                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('login'))
    # rendering login page
    return render_template('login.html', form = form)

@app.route('/logout/')
def logout():
    # Removing data from session by setting logged_flag to False.
    session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run()
