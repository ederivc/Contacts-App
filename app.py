import os
import re
import uuid
import bcrypt
import mysql.connector as mysql
from restorePw import send_email
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, request, redirect, session, flash
from validations import (validate, validate_email, validate_existing_email, validate_token, 
                        validate_user, validate_image, validate_contact, validate_existing_image) 

app = Flask(__name__)
app.secret_key = "hola"
connection = mysql.connect(host='localhost',
                        user='root',
                        passwd='',
                        database='userContacts')

app.config["IMAGE_UPLOADS"] = "/home/peppa/Documentos/Python/Contacts-App-master/static/img/upload"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_IMAGE_FILESIZE"] = 3 * 1024 * 1024


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
            return render_template("profile.html", info = get_info(), image = get_image())
        else:
            username = request.form["username"]
            password = request.form["password"]

            x = validate(username, password, connection)

            if x == True:
                session['username'] = username
                session['password'] = password

                flash('You were successfully logged in')
                return render_template("profile.html", info = get_info(), image = get_image())
            else:
                flash('Incorrect data, try again.', 'error')
                return redirect(url_for("login"))
    #Dude
    else:
        if 'username' in session:
            return render_template("profile.html", info = get_info(), image = get_image())
        else:
            return redirect(url_for("login"))
            

#Return Add contact template
@app.route('/add', methods=["POST", "GET"])
def add():
    if 'username' in session:
        return render_template('addContact.html')


#Add new contact
@app.route('/insertContact', methods=["POST", "GET"])
def insertContact():
    if 'username' in session:
        if request.method == "POST":

            user = session["username"]
            contact_name = request.form["contact_name"]
            contact_phone = request.form["contact_phone"]

            if not contacts_format(contact_name, contact_phone):
                flash("Invalid format", "error")
                return redirect(url_for("profile"))

            if not validate_contact(user, contact_phone, connection):
                flash("Duplicated contact", "error")
                return redirect(url_for("profile"))

            dir = connection.cursor(buffered=True)
            dir.execute("SELECT UserId FROM Users WHERE Username = %s",(user,))
            _id = dir.fetchone()

            dir = connection.cursor(buffered=True)
            dir.execute("INSERT INTO Contacts (user_id, ContactName, ContactPhone) VALUES" +
            "(%s, %s, %s)",(_id[0], contact_name, contact_phone))


            connection.commit()
            flash("Contact added successfully", 'message')
            return redirect(url_for("profile"))

        else:
            return render_template("addContact.html")


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

        dir = connection.cursor(buffered=True)
        dir.execute("""SELECT COUNT(ContactName) FROM Contacts WHERE
        user_id = (SELECT UserId FROM Users WHERE Username = %s)""", 
        (user,))
        length = dir.fetchone()
        x = int(length[0])

        return render_template('contacts.html', values = values, length = x)
    
    else:
        return redirect(url_for("login"))


#Search contacts
@app.route("/search", methods=["POST", "GET"])
def search_contacts():
    if "username" in session:
        if request.method == "POST":
            user = session["username"]
            search_names = request.form["search"]

            dir = connection.cursor()
            dir.execute("""SELECT * FROM Contacts WHERE user_id =  
            (SELECT UserId FROM Users WHERE Username = %s) AND ContactName 
            LIKE %s """, (user, "%" + search_names + "%"))
            values = dir.fetchall() 

            return render_template('search.html', values = values) 
        return redirect(url_for("display_info"))


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
            flash("You are already logged in")
            return redirect(url_for("profile"))

        else:
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            con_password = request.form["conf-password"]
            email = request.form["email"]

            x = validate_user(username, password, con_password, name, connection)
            email_ver = validate_email(email, connection)

            if x == True and email_ver == True:
                hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

                dir = connection.cursor(buffered=True)
                dir.execute("""INSERT INTO Users (Username, Password, Name, Email) 
                VALUES (%s, %s, %s, %s)""", (username, hashed, name, email))
                connection.commit() 

                flash("Cuenta creada correctamente")
                return redirect(url_for("login"))

            else:
                return redirect(url_for("add_newUser"))

    else:
        if 'username' in session:
            return redirect(url_for("profile")) 


#Edit contact
@app.route("/editContact/<act_phone>", methods=["POST"])
def editContact(act_phone):
    if 'username' in session:
        if request.method == "POST":
            name = request.form["con_name"]
            phone = request.form["con_phone"]

            if not contacts_format(name, phone):
                flash("Invalid format", "error")
                return redirect(url_for("display_info"))

            try:
                dir = connection.cursor(buffered=True)   
                dir.execute("UPDATE Contacts SET ContactName = %s, ContactPhone = %s " +
                "WHERE ContactPhone = %s", (name, phone, act_phone))

                connection.commit()

                flash('User modified successfully')
                return redirect(url_for("display_info"))

            except Exception as e:
                print(e)
                flash("Erroooooor", 'error')
                return redirect(url_for("login"))


#Delete contact
@app.route("/delete/<contact>")
def delete(contact):
    if 'username' in session:
        try:
            dir = connection.cursor() 
            dir.execute("DELETE FROM Contacts WHERE ContactId = %s",(contact,)) 
            connection.commit()

            flash("Eliminado", 'message')
            return redirect(url_for("display_info"))

        except Exception as e:
            print("Failed to insert record into Product table {}".format(e))
            flash('Error')


#Request password
@app.route("/requestPassword", methods=["POST", "GET"])
def requestPassword():
    if 'username' in session:
        return redirect(url_for("profile"))
    else:
        if request.method == "POST":
            #Here
            email = request.form["email"]
            user_email = validate_existing_email(email, connection)

            if user_email != False:
               
                send_email(user_email, connection)


                flash("Email sent")
                return redirect(url_for("login"))

            else:
                flash("Email not found", 'error')
                return redirect(url_for("login"))

        else:
            return render_template("requestPassword.html")


#Reset password
@app.route("/reset/<token>", methods=["POST", "GET"])
def resetPassword(token):
    if 'username' in session:
        return redirect(url_for("profile"))
    else:
        if request.method == "POST": 

            password = request.form["password"]
            conf_password = request.form["conf-password"]

            if password != conf_password: 
                flash("Password don't match.")
                return redirect("resetPassword")

            hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            new_token = str(uuid.uuid4())
            
            dir = connection.cursor()
            dir.execute(""" SELECT * FROM Users WHERE 
            Token = %s """,(token,))
            user = dir.fetchone()

            if user:
                dir = connection.cursor()
                dir.execute(""" UPDATE Users SET Password = %s,
                Token = %s WHERE Token = %s """,(hashed, new_token,
                token))
                connection.commit()

                return redirect(url_for("login"))

            else:
                return redirect(url_for("login"))

        else:
            x = validate_token(token, connection)

            if x == True:
                return render_template("resetPw.html")
            else:
                flash("Page not found, try again.", "error")
                return redirect(url_for("login"))


#Upload image
@app.route("/upload-image", methods=["POST", "GET"])
def upload_image():
    if "username" in session:
        if request.method == "POST":
            if request.files:
                
                if not allowed_image_size(request.cookies["filesize"]):
                    flash("The image exceeded maximum size", "error")
                    return redirect(url_for("profile"))

                user = session['username']
                image = request.files["image"]

                if image.filename == "":
                    flash("Image must have a name", "error")
                    return redirect(url_for("profile"))

                if not validate_image(image.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
                    flash("Incorrect file", "error")
                    return redirect(url_for("profile"))
                else:
                    old_path = get_image_path(user)
                    filename = secure_filename(image.filename)

                image_url = os.path.join("/static/img/upload", filename)

                dir = connection.cursor(buffered=True)
                dir.execute("""UPDATE Users SET ImagePath = %s WHERE
                Username = %s""",(image_url, user))
                connection.commit()

                existing_path = validate_existing_image(old_path, connection)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                return redirect(url_for("profile"))

        return redirect(url_for("login"))  
    
    return redirect(url_for("login"))


def allowed_image_size(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

#Get user info
def get_info():
    if 'username' in session:
        user = session['username']

        dir = connection.cursor(buffered=True)
        dir.execute("""SELECT Username, Name, Email FROM Users WHERE
        Username = %s """, (user,))
        value = dir.fetchall()

        return value[0]


#Get user image
def get_image():
    if "username" in session:
        user = session["username"]

        dir = connection.cursor(buffered=True)
        dir.execute("""SELECT ImagePath FROM Users WHERE
        Username = %s """, (user,))
        value = dir.fetchone()

        if value[0] == None:
            return "https://cdn2.iconfinder.com/data/icons/people-80/96/Picture1-512.png"
        else:
            return str(value[0])


def get_image_path(user):
    dir = connection.cursor()
    dir.execute(""" SELECT ImagePath FROM Users WHERE User = %s """, (user,))
    path = dir.fetchone()

    if path[0] == None:
        return "/static/img/upload/anything"
    else:
        return path[0]
    

def contacts_format(name, phone):
    name_val = re.match(r"[a-zA-Z]{1,30}$", name)
    phone_val = re.match(r"\d{10}$", phone)
    #phone_val = re.match(r"\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$", contact_phone)

    if not name_val or not phone_val:
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(debug=True)
    index()
