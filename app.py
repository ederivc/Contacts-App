from flask import Flask, render_template, url_for, request, redirect, session
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
    return render_template('index.html')


#Home page where the user type the data
@app.route('/home', methods=["POST"])
def login():
    return render_template('login.html')


#Log out 
@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))
    

#Profile page where the user can choose the options
@app.route('/profile', methods=["POST"])
def profile():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        x = validate(username, password)

        if x == True:
            session['username'] = username
            session['password'] = password

            return render_template("profile.html")
        else:
            print("Incorrect data")
            return render_template("login.html")
    #Dude
    else:
        return render_template("profile.html")


#Redirect in order to add a new contact
@app.route('/redirect', methods=["POST"])
def _redirect():
    if 'username' in session:
        return render_template('addContact.html')


#Add new contact
@app.route('/add', methods=["POST"])
def add():
    if 'username' in session:
        if request.method == "POST":

            user = session["username"]
            contact_name = request.form["contact_name"]
            contact_phone = request.form["contact_phone"]

            dir = connection.cursor(buffered=True)
            dir.execute("SELECT UserId FROM Users WHERE Username = %s",(user,))
            _id = dir.fetchone()

            dir = connection.cursor(buffered=True)
            #INSERT INTO `Contacts` (`ContactId`, `user_id`, `ContactName`, `ContactPhone`) VALUES (NULL, '4', 'Pedro', '333422323');
            dir.execute("INSERT INTO Contacts (user_id, ContactName, ContactPhone) VALUES" +
            "(%s, %s, %s)",(_id[0], contact_name, contact_phone))

            connection.commit()
            return render_template("profile.html")


#Page in which the info is displayed
@app.route('/contacts', methods=["POST"])
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
    

if __name__ == "__main__":
    app.run(debug=True)
    index()
