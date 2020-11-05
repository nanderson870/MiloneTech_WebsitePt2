from flask import render_template, url_for, flash, redirect, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
import json

from matplotlib.pyplot import figure
from Website_Python_Code.flask_website.forms import RegistrationForm, LoginForm

from Website_Python_Code.flask_website import app, bcrypt, db



exampleSensorData = [
    {
        "sensorID":"157.111.521.457",
        "sensorName":"Water Tank",
        "groupString":"WaterTankers",
        "batteryLevel":"80%",
        "typeOfSensor":"water",
        
        "x" : [1,2,3,4,5,6], 
        "y" : [0.80,0.0,0.70,0.0,0.60,0.55], 
  
    },
    {
        "sensorID":"455.999.521.457",
        "sensorName":"Vat of Acid",
        "groupString":"WaterTankers",
        "batteryLevel":"75%",
        "typeOfSensor":"chemical",
        
        "x" : [1,2,3,4,5,6], 
        "y" : [0.80,0.50,0.50,0.70,0.20,0.15] 
  
    },
    {
        "sensorID":"455.999.521.457",
        "sensorName":"Showing Chu",
        "groupString":"WaterTankers",
        "batteryLevel":"75%",
        "typeOfSensor":"chemical",
        
        "x" : [1,2,3,4,5,6], 
        "y" : [0.0,0.90,0.50,0.70,0.20,0.0] 
  
   }
    
]

targetEmail = ""

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    
    global targetEmail
    form = LoginForm()
    
    if form.validate_on_submit():
        if bcrypt.check_password_hash(db.getUserPassword(form.email.data), form.password.data):
            flash('You have been logged in!', 'success')
            targetEmail = str(form.email.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route("/home")
def home():
    
    global targetEmail
    currUserSensors = []
    currUserSensorData = []
    
    
    if targetEmail != "":
        currUserSensors = db.getAllSensors(targetEmail)
    else:
        currUserSensors = ["001"]
    
    print(currUserSensors)
     
    for i in range(0,len(currUserSensors)):
        
        
        currUserSensorData.append(db.getSensorDataPoints(currUserSensors[i]))
    

    print(currUserSensorData)
    #CODE FOR GENERATING THE PLOTS
    
    for i in range(0,len(currUserSensorData)):
    
        fig = Figure()
        plt = fig.add_subplot(1,1,1)
        
        targetSensorData = exampleSensorData[i]
        plt.set_ylim(0,1)
        plt.set_xlim(0,6)
        # naming the x axis 
        plt.set_xlabel('Reading Times') 
        # naming the y axis 
        plt.set_ylabel('Sensor Levels') 
          
        # giving a title to my graph 
        plt.set_title('Sensor data for %s' % currUserSensorData[i]["sensorID"]) 
        
        plt.plot(currUserSensorData[i]["x_vals"], currUserSensorData[i]["y_vals"], color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12) 
        
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
    
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        currUserSensorData[i]["image"] = pngImageB64String
        
    
    
    return render_template('home.html', exampleSensorData=currUserSensorData)

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    global db
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.createNewAccount(accountEmail = form.email.data, password = hashed_pass, name = form.fullname.data)
        
        flash(f'Your account has been Created! You may now Login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


# SAMPLE
@app.route("/sensor", methods=['POST'])
def sensor():
    
    sensor_msg = request.json
    db.setSensorInfo(sensor_msg["Sensor ID"], sensor_msg["Liquid %"],sensor_msg["Battery %"],sensor_msg["Time Stamp"])
    
    return "OK"

@app.route("/account", methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if db.getUserPassword(form.email.data) == form.password.data:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('account.html', title='Account', form=form)


@app.route("/settings", methods=['GET', 'POST'])
def settings():
        form = SettingsForm()
        if form.validate_on_submit():
                if db.getUserPassword(form.email.data) == form.password.data:
                        flash('You have been logged in!', 'success')
                        return redirect(url_for('home'))
                else:
                        flash('Login Unsuccessful. Please check username and password', 'danger')

        return render_template('settings.html', title='Settings', form=form)