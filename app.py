from flask import Flask, render_template, url_for, request, redirect
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = "hola"
connection = mysql.connect(host='localhost',
                        user='root',
                        passwd='',
                        database='userContacts')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def login():
    return render_template('login.html')


@app.route('/profile', methods=["POST"])
def profile():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        values = [username, password]

        return render_template("profile.html", values = values)


@app.route('/contacts')
def display_info():
    pass

if __name__ == "__main__":
    app.run(debug=True)
    index()
