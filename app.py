from flask import Flask, render_template, url_for, request, redirect, session, flash
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = "hola"
connection = mysql.connect(host='localhost',
                        user='root',
                        passwd='',
                        database='userContacts')

#Main page
@app.route('/')
def index():
    if 'username' not in session:
        return render_template('index.html')
    else:
        session.pop("username", None)
        return render_template('index.html')
    


#Home page where the user type the data
@app.route('/home', methods=["POST", "GET"])
def login():
    return render_template('login.html')


#Log out 
@app.route('/logout', methods=["GET"])
def logout():
    if request.method == "GET":
        if 'username' not in session:
            flash("You are not logged in", 'error')
            return redirect(url_for("login"))
        else:
            flash("You were succesfully logged out", 'message')
            session.pop("username", None)
            return redirect(url_for("index"))
    

#Profile page where the user can choose the options
@app.route('/profile', methods=["POST", "GET"])
def profile():
    if request.method == "POST":
        if 'username' in session:
            return render_template("profile.html")
        else:
            username = request.form["username"]
            password = request.form["password"]

            x = validate(username, password)

            if x == True:
                session['username'] = username
                session['password'] = password

                flash('You were successfully logged in')
                return render_template("profile.html")
            else:
                flash('Incorrect data, try again.', 'error')
                return redirect(url_for("login"))
    #Dude
    else:
        if 'username' in session:
            #flash("You are already logged in.", 'message')
            return render_template("profile.html")
        else:
            #flash("You are already logged in.", 'message')
            return redirect(url_for("login"))
            

#Return Add contact template
@app.route('/add', methods=["POST"])
def add():
    if 'username' in session:
        return render_template('addContact.html')


#Add new contact
@app.route('/insertContact', methods=["POST", "GET"])
def insertContact():
    if request.method == "POST":
        if 'username' in session:

            user = session["username"]
            contact_name = request.form["contact_name"]
            contact_phone = request.form["contact_phone"]

            dir = connection.cursor(buffered=True)
            dir.execute("SELECT UserId FROM Users WHERE Username = %s",(user,))
            _id = dir.fetchone()

            dir = connection.cursor(buffered=True)
            dir.execute("INSERT INTO Contacts (user_id, ContactName, ContactPhone) VALUES" +
            "(%s, %s, %s)",(_id[0], contact_name, contact_phone))

            connection.commit()
            return redirect(url_for("profile"))


#Page in which the info is displayed
@app.route('/contacts', methods=["POST", "GET"])
def display_info():
    if 'username' in session:
        user = session["username"]
        password = session["password"]

        values = [user, password]
        dir = connection.cursor()
        dir.execute("SELECT * FROM Contacts WHERE user_id =" +
        "(SELECT UserId FROM Users WHERE Username = %s)", (user,))
        values = dir.fetchall()  

        return render_template('contacts.html', values = values)
    
    else:
        return redirect(url_for("login"))


#Return new user template
@app.route('/newUser', methods=["POST", "GET"])
def add_newUser():
    if 'username' in session:
        return redirect(url_for("profile")) 
    else:
        return render_template("newAccount.html")


#New user
@app.route("/insertUser", methods=["POST", "GET"])
def insertUser():
    if request.method == "POST":
        if 'username' in session:
            print("You are already logged in")
            return redirect(url_for("profile"))

        else:
            username = request.form["username"]
            password = request.form["password"]
            con_password = request.form["password2"]

            x = validate_user(username, password, con_password)

            if x == True:
                dir = connection.cursor(buffered=True)
                dir.execute("INSERT INTO Users (Username, Password) VALUES " +
                "(%s, %s)", (username, password))
                print("Added")
                connection.commit()
                return redirect(url_for("login"))

            else:
                print("Error")
                return redirect(url_for("login"))

    else:
        if 'username' in session:
            return redirect(url_for("profile"))


#Validate the user when login
def validate(username, password):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Username FROM Users WHERE Username = %s",(username,)) 
    value = dir.fetchone()

    if not value:
        return False

    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Password FROM Users WHERE Password = %s",(password,))
    value = dir.fetchone()
    if not value:
        return False

    return True
    

#Validate if the user exists and the passwords match
def validate_user(username, password, con_password):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Username FROM Users WHERE Username = %s",(username,)) 
    value = dir.fetchone()

    if not value and password == con_password:
        if value == "" or password == "":
            return False
        print("Correct")
        return True

    return False


if __name__ == "__main__":
    app.run(debug=True)
    index()
