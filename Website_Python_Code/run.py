#from moda import funca
#funca()
#exit(0)


from flask_website import app

import os

if __name__ == '__main__':
    print("getcwd():", os.getcwd())
    app.run(debug=True)
