# set up database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database_name"
)

# check database connection
if mydb.is_connected():
    print("Connected to database")

# retrieve form data
username = request.form['username']
email = request.form['email']
password = request.form['password']
phone = request.form['phone']

# prepare SQL statement
mycursor = mydb.cursor()
sql = "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)"
val = (username, email, password, phone)

# execute SQL statement
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")

# close statement and database connection
mycursor.close()
mydb.close()
