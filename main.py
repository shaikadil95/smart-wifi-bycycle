from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            idd = 1
            active_session = session['id']
            #updates id for sensor readings
            cur = mysql.connection.cursor()
            cur.execute("UPDATE testtable SET sessionid = %s WHERE id=%s", (active_session, idd))
            mysql.connection.commit()
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, 0, 1, 0)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        #User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        time_available = cursor.fetchone()
        return render_template('home.html', username=session['username'], time_available=time_available)
    #User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile', methods=['GET', 'POST'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/requestedtime', methods=['GET', 'POST'])
def timereqest():
    if 'loggedin' in session:
        if request.method == 'POST' and 'timerequest' in request.form:
            datafetch = (request.form['timerequest'])
            data = int(datafetch)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT timeavailable FROM accounts WHERE id = %s', [session['id']])
            availabledata = cursor.fetchone()
            for row, value in availabledata.items():
                available = value
            if data <= available:
                newdata = available - data
                id_id = session['id']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE accounts SET timeavailable = %s WHERE id=%s", (newdata, id_id))
                mysql.connection.commit()
                msg = ("Good to Go!")
            else:
                msg = ("Requested time is more than available time")
            return  render_template('requestedtime.html', msg=msg)

    return redirect(url_for('login'))


@app.route('/adminlogins', methods=['GET', 'POST'])
def adminlogins():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['Adminloggedin'] = True
            return redirect(url_for('adminpage'))
    return render_template('adminlogin.html', error=error)

@app.route('/adminpage')
def adminpage():
    # Check if user is loggedin
    if 'Adminloggedin' in session:
        # User is loggedin show them the home page
        return render_template('adminpage.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/fetching')
def Index():
    if 'Adminloggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM accounts")
        data = cur.fetchall()
        cur.close()
        return render_template('index2.html', students=data )
    return redirect(url_for('login'))


@app.route('/insert', methods = ['POST'])
def insert():
    if 'Adminloggedin' in session:
        if request.method == "POST":
            flash("Data Inserted Successfully")
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            timeavailable = request.form['timeavailable']
            criteria = request.form['criteria']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO accounts (username, password, email, timeavailable, criteria, steps) VALUES (%s, %s, %s, %s, %s, 0)", (username, password, email, timeavailable, criteria))
            mysql.connection.commit()
            return redirect(url_for('Index'))
    return redirect(url_for('login'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    if 'Adminloggedin' in session:
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM accounts WHERE id=%s", (id_data,))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    return redirect(url_for('login'))


@app.route('/update',methods=['POST','GET'])
def update():
    if 'Adminloggedin' in session:
        if request.method == 'POST':
            id_data = request.form['id']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            timeavailable = request.form['timeavailable']
            criteria = request.form['criteria']
            cur = mysql.connection.cursor()
            cur.execute("""
                   UPDATE accounts
                   SET username=%s, password=%s, email=%s, timeavailable=%s, criteria=%s, steps=0
                   WHERE id=%s
                """, (username, password, email, timeavailable, criteria, id_data))
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('Index'))
    return redirect(url_for('login'))


@app.route('/adminlogouts')
def adminlogout():
    # Remove session data, this will log the user out
   session.pop('Adminloggedin', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/workoutsession')
def sensorStart():
    msgSensor = "Workout session started Please start pedalling"
    return render_template('startSensor.html', msgSensor=msgSensor)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
