from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text.db'
app.config['SECRET_KEY'] = '63103453574bccae5541fa05'
db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(), unique = True, nullable = False)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    def __repr__(self):
        return f'<Account {self.username}>'

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key = True)
    msg = db.Column(db.String(),unique = False, default = " ")
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=date.today)


@app.route('/home')
@app.route('/')
def home():
    messages = Message.query.all()
    users = Account.query.all()
    messages.reverse()
    return render_template('index.html', messages=messages, users=users)

@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')
    user = Account.query.filter_by(email=email, password=password).first()
    if user:
        username = user.username
        print(username)
        session['username'] = username
        session['email'] = email
        return redirect(url_for('home'))
    
    return render_template('sign-in.html')

@app.route('/sign-out')
def sign_out():
    session.pop("email", None)
    return redirect('/')

@app.route('/post', methods=['POST', 'GET'])
def post():
    
    username = session.get('username')
    msg = request.form.get("message")
    create = request.form.get("send", False)
    if (msg != ' '):
        if(create != False):
            sender = Account.query.filter_by(username=username).first()
            post = Message(msg = msg, sender_id = sender.id)
            db.session.add(post)
            db.session.commit()
    return render_template("post.html",username=username)


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        psw = request.form.get("password")
        psw_confirm = request.form.get("confirm-password")
        # Check if username already exists
        if Account.query.filter_by(username=username).first():
            return render_template('register.html', message="Username already exists.")
        if Account.query.filter_by(email=email).first():
            return render_template('register.html', message="Another account is using this email.")
        if psw != psw_confirm:
            return render_template('register.html', message = "The passwords does not match")
        # Create new account
        new_account = Account(email=email, username=username, password=psw)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')
if __name__ == "__main__":
    app.run(debug=True)









