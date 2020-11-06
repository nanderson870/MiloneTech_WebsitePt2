from flask import Flask
from flask_bcrypt import Bcrypt
import Website_Python_Code.flask_website.fakedb as db
#from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)

from Website_Python_Code.flask_website import routes