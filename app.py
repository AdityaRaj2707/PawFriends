from flask import Flask, render_template, request, session
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "raj&team"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abcd$1234'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route("/")
def home():
    # if not session.get('loggedin'):
    #     return redirect(url_for('login'))  
    name = session.get('username')  
    return render_template("home.html", name=name)
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return redirect(url_for('home'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('home'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		pettype = request.form['pettype']
		petname = request.form['petname']
		breed= request.form['breed']
		dob=request.form['dob']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s,% s,% s,% s,% s)', (username, password, email,pettype,petname,breed,dob ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route("/health")
def health():
    return render_template("health.html")

@app.route("/training")
def training():
    return render_template("training.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/breeds")
def breeds():
    return render_template("breeds.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/emergencies")
def emergencies():
    return render_template("emergencies.html")

# @app.route("/snl")
# def snl():
#     return render_template("snl.html")


# create connection to database
# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# # create users table
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (username TEXT, email TEXT, password TEXT, phone TEXT)''')
# conn.commit()

# @app.route('/snl')
# def snl():
#     return render_template('snl.html')

# @app.route('/signup', methods=['POST'])
# def signup():
#     # get user inputs from form
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     phone = request.form['phone']

#     # insert user data into database
#     c.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
#               (username, email, password, phone))
#     conn.commit()

#     return redirect(url_for('/snl'))


if __name__ == "__main__":
    app.run(debug=True)


