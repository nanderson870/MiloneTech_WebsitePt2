import Website_Python_Code.flask_website.dbAPI.app as app
import flask_bcrypt as bcrypt

if app.accounts.create_account("lgrebe","Lucas",
                        "Grebe",bcrypt.generate_password_hash("lucasgrebe").decode("utf-8")):
    print("acc made")
else:
    print("fuck up")