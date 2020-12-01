import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "milonetechnotifications@gmail.com"
password = "SEGroupIV"
# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
def send_password_request(to_email, redirect_address):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset from UsersMiloneTech.com"
    message["From"] = sender_email
    message["To"] = to_email

    text = f'''
To reset your password, visit the following link: 
{redirect_address}
    
If you did not make this request, then simply ignore this email and no changes will be made
    '''

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    send_mail(to_email,message)


def send_email_notification(to_email, sensor, curr_user_name, alert_level, curr_level):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Liquid Level alert from UsersMiloneTech.com"
    message["From"] = sender_email
    message["To"] = to_email

    text = f'''
ATTENTION {curr_user_name}, we have just gotten a reading from your sensor, {sensor}
and it has reached below its designated alert level of {alert_level} to {curr_level}

Please check it if you see fit.
Have a great day!
    '''

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    send_mail(to_email, message)


def send_mail(to_email, message):

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)

        server.sendmail(sender_email, to_email, message.as_string())

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


'''
text = """\
    Your sensor %s has gone below the level of %s

    You can check on your liquid levels usersmilonetech.com

    """

    html = """\
    <html>
      <body>
        <p>
            Your sensor %s has gone below its set notification level. <br>
            <br>
                sensor name: <br>
                level: %s <br>
                at time: %s <br>
            <br>
            You can check on your liquid levels at <a href="usersmilonetech".com> usersmilonetech.com </a><br>
            <br>
            Sent 
        </p>
      </body>
    </html>
    """

'''