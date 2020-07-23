import re
import os
import bcrypt
from flask import Flask, flash
import mysql.connector as mysql
 
#Validate email
def validate_email(email, connection):
    val = re.match(r'[\w-]{1,20}@\w{2,20}\.(com|edu|net)$', email)
    if val:
        dir = connection.cursor(buffered=True)
        dir.execute("SELECT Email FROM Users WHERE Email = %s", (email,))
        value = dir.fetchone()

        if not value:
            return True
        else:
            flash("El correo ya existe", 'error')
            return False
    else:
        flash("El email esta en un formato incorrecto", 'error')
        return False


#Validate the user when login
def validate(username, password, connection):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Username FROM Users WHERE Username = %s",(username,)) 
    value = dir.fetchone()

    if not value:
        return False

    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Password FROM Users WHERE Username = %s",(username,))
    value = dir.fetchone()

    if not value:
        return False
    else:
        if bcrypt.checkpw(password.encode('utf8'), value[0].encode('utf8')):
            return True
    

#Validate if the user exists and the passwords match
def validate_user(username, password, con_password, name, connection):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Username FROM Users WHERE Username = %s",(username,)) 
    value = dir.fetchone()

    if not value and password == con_password:
        if value == "" or password == "" or name == "":
            flash("No puedes dejar espacios en blanco", 'error')
            return False
        return True

    flash("El usuario ya existe", 'error')
    return False


#Validate existing email
def validate_existing_email(email, connection):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT Email FROM Users WHERE Email = %s", (email,))
    value = dir.fetchone()

    if not value:
        return False

    else:
        return value[0]


#Validate token
def validate_token(token, connection):
    dir = connection.cursor(buffered=True)
    dir.execute("SELECT * FROM Users WHERE Token = %s", (token,))
    value = dir.fetchone()

    if not value:
        return False

    else:
        return True

#Validate contact
def validate_contact(user, phone, connection):
    dir = connection.cursor()
    dir.execute("""SELECT ContactPhone FROM Contacts WHERE user_id = 
    (SELECT UserId FROM Users WHERE Username = %s) AND ContactPhone = %s""", (user, phone))
    value = dir.fetchone()      
    #print(value[0])
    if not value:
        return True
    else:
        return False


def validate_image(filename, config):
    if not "." in filename:
        return False
    
    extension = filename.rsplit(".", 1)[1] 

    if extension.upper() in config:
        return True
    else:
        return False

"""def validate_existing_image(old_image_path, complete_image_url, connection):
    dir = connection.cursor()
    dir.execute(""""""SELECT ImagePath FROM Users WHERE ImagePath LIKE  
    %s """""",("%" + old_image_path,))
    path = dir.fetchone()

    print("aqui")
    print(path)

    if path == None:
        print("no",complete_image_url)
        if os.path.exists(complete_image_url):
            os.remove(complete_image_url)
        else:
            pass
    else:
        if old_image_path == "/static/img/upload/anything":
            pass
        else:
            print(complete_image_url)
            if os.path.exists(complete_image_url):
                os.remove(complete_image_url)
            else:
                pass"""

def validate_existing_image(old_image_path, complete_image_path, connection):
    if old_image_path == "/static/img/upload/anything":
        pass
    else:
        dir = connection.cursor()
        dir.execute("""SELECT Username FROM Users WHERE ImagePath LIKE
        %s """,("%" + old_image_path,))
        path = dir.fetchall()
        
        if not path:
            if os.path.exists(complete_image_path):
                os.remove(complete_image_path)
            else:
                pass

        else:
            pass
