import uuid
import smtplib
from email.message import EmailMessage

def send_email(email, connection):
    email_address = "PruebapPy.00@gmail.com"
    password = '1234E4321e'

    token = str(uuid.uuid4())
    print(type(token))

    dir = connection.cursor(buffered=True)
    dir.execute(""" UPDATE Users SET Token = %s WHERE
    Email = %s""",(token, email))
    connection.commit()

    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(f"""To reset your password, please visit the
    following link: 127.0.0.1:5000/reset/{token}
    
    If you did not make this request then simply 
    ignore this email and no changes will be made.""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(msg)
