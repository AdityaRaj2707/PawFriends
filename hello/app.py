import smtplib
from flask import Flask, render_template, request, session
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import secure as q

app = Flask(__name__)
app.secret_key = "raj&team"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abcd$1234'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route("/")
def home(): 
    name = session.get('username')  
    if name !=None:
       name = name.upper()
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

@app.route('/doclogin', methods =['GET', 'POST'])
def doclogin():
	msg = ''
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM doctors WHERE email = % s AND password = % s', (email, password))
		doctor = cursor.fetchone()
		if doctor:
			session['docloggedin'] = True
			session['docusername'] = doctor['name']
			msg = 'Logged in successfully !'
			return redirect(url_for('doctor'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('doclogin.html', msg = msg)

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

@app.route('/docregister', methods =['GET', 'POST'])
def docregister():
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		phone_num = request.form['phone']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM doctors WHERE email = % s', (email, ))
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
			cursor.execute('INSERT INTO doctors VALUES (NULL, % s, % s, % s,% s)', (username,  email, password, phone_num))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('docregister.html', msg = msg)

@app.route("/health")
def health():
    return render_template("health.html")

@app.route("/appointment", methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        petname = request.form['petName']
        owner = request.form['ownerName']
        email = request.form['email']
        phone = request.form['phone']
        adate = request.form['date']
        atime = request.form['time']
        docname = request.form['doctor']
        psw = request.form['pasw']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (owner, psw))
        account = cursor.fetchone()
        cursor.execute('SELECT email, phone FROM doctors WHERE name = %s', (docname,))
        docmail = cursor.fetchone()
        docphone = docmail['phone']
        docemail = docmail['email']
        print(docmail['email'])
        print("hello")

        if account:
            sender_email = q.mail
            password = q.psw
            message = f"""
            Hello Doctor, a new Pet Appointment is created, now on Pawfriend.com with { owner } for their pet {petname} on {adate} at {atime}.\nTheir contact details are {phone} and {email}.
	    ThankYou\n
	    With Regards,
	    PawFriend Org
            """
            message2 = f"""
            Hello Customer, your Pet Appointment is successfully created, on Pawfriend.com with { docname } for your pet {petname} on {adate} at {atime}.\n Doctor's contact details are {docphone} and {docemail}.
	    ThankYou\n
	    With Regards,
	    PawFriend Org
            """
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, docemail, message)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message2)
		
		
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO appointments VALUES (NULL, % s, % s, % s, % s, % s, % s, % s)', (petname,owner, email, phone, adate, atime, docname))
            mysql.connection.commit()
            return redirect('/')
        else:
                return redirect(url_for('login'))
    return render_template("appointment.html")


@app.route('/doctor')
def doctor():
    name = session['docusername']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# cursor.execute('SELECT * FROM doctors WHERE email = % s', (email, ))

    # mycursor = mydb.cursor()

    # Retrieve all appointments for the current doctor
    doctor_id = 1 # replace with the current doctor's ID
    cursor.execute("SELECT pet_name, owner_name, email, phone, appointment_date, appointment_time FROM appointments WHERE doctor_name = %s", (name,))
    appointments = cursor.fetchall()

    # Render the appointments page and pass the appointments to the template
    return render_template('doctor.html', appointments=appointments, name=name)

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


