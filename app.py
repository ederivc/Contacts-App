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

        session['username'] = username
        session['password'] = password

        return render_template("profile.html")


#Page in which the info is displayed
@app.route('/contacts', methods=["POST"])
def display_info():
    if 'username' in session:
        user = session["username"]
        password = session["password"]

        values = [user, password]

        return render_template('contacts.html', values = values)


#Add new contact
@app.route('/add')
def add_contact():
    pass

if __name__ == "__main__":
    app.run(debug=True)
    index()
