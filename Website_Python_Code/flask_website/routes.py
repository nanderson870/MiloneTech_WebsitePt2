from flask import render_template, url_for, flash, redirect, Response, request
'''from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import figure
'''
import datetime
import io
import base64
import json
from flask_website.forms import RegistrationForm, LoginForm, SettingsForm, AccountForm
from flask_website import app, bcrypt, db, login_manager

from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from pprint import pprint

class User(UserMixin):

    def initialize_user_data(self):

        # Getting Sensors for Account
        data = {}

        data["email"] = self.email
        data["payment_tier"] = db.accounts.get_status_by_id(self.id)[0]
        data["sensor_data"] = dict()
        curr_user_sensors = db.sensors.get_all_sensors(self.id)

        curr_user_groups = {}

        # find all groups for current user
        for sensor in curr_user_sensors:

            curr_group = db.sensors.get_sensor_info(sensor)[0][6]

            if curr_group != None:
                if curr_group not in curr_user_groups:

                    temp_list = []
                    temp_list.append(sensor)
                    curr_user_groups[curr_group] = temp_list

                else:

                    curr_user_groups[curr_group].append(sensor)
            else:
                if "No Group" not in curr_user_groups:

                    temp_list = []
                    temp_list.append(sensor)
                    curr_user_groups["No Group"] = temp_list

                else:

                    curr_user_groups["No Group"].append(sensor)

        for group in curr_user_groups:

            '''[(535, '100', 10, 'norm', 'water_tower1', 60, None)]'''
            group_list = curr_user_groups[group]
            data["sensor_data"][group] = {}

            for sensor in group_list:

                curr_sensor = {}
                sensor_data = db.sensors.get_sensor_info(sensor)[0]

                curr_sensor["name"] = sensor_data[4]
                curr_sensor["x_vals"] = []
                curr_sensor["y_vals"] = []
                curr_sensor["bat_level"] = db.sensor_readings.get_sensor_battery(sensor)

                sensor_values = db.sensor_readings.get_sensor_data_points(sensor)
                counter = 0

                for data_point in sensor_values:
                    '''
                    curr_sensor["x_vals"] = data_point[5]
                    '''
                    curr_sensor["x_vals"].append(counter)
                    curr_sensor["y_vals"].append(data_point[3])
                    counter = counter + 1

                data["sensor_data"][group][sensor] = curr_sensor

        return data

    def __init__(self, userID):
        self.id = userID
        self.email = db.accounts.get_email_by_id(userID)[0]
        self.user_data = self.initialize_user_data()


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        userID = db.accounts.get_id_by_email(form.email.data)[0]
        user = User(userID)


        if user and bcrypt.check_password_hash( db.accounts.get_pass_by_id(userID)[0], form.password.data):

            print("almost there")
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')

            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route("/home")
@login_required
def home():

    return render_template('home.html', account_info=current_user.user_data)

@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        fullname = form.name.data.split()
        firstname = fullname[0]
        lastname = fullname[-1]

        db.accounts.create_account(form.email.data,firstname,lastname,hashed_pass)
        
        flash(f'Your account has been Created! You may now Login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


# SAMPLE
@app.route("/sensor", methods=['POST'])
def sensor():

    data_string = "Recieved post at: %s\n" % datetime.datetime.now()
    print(data_string)
    data = request.json
    data_string = data_string + str(data) + "\n"

    with open('./flask_website/records.txt', 'a') as f:
        f.write(data_string)

    sensorID = data["Sensor ID"]

    for entry in data["Sensor Data"]:
        db.sensor_readings.add_reading_no_time(sensorID, entry["Liquid %"], entry["Battery %"],
                                               entry["RSSI"])

    return db.sensors.get_sensor_time_between(sensorID)

@app.route("/account", methods=['GET', 'POST'])
@login_required
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
@login_required
def settings():

        form = SettingsForm()
        if form.validate_on_submit():
                if db.getUserPassword(form.email.data) == form.password.data:
                        flash('You have been logged in!', 'success')
                        return redirect(url_for('home'))
                else:
                        flash('Login Unsuccessful. Please check username and password', 'danger')

        return render_template('settings.html', title='Settings', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

'''fig = Figure()
plt = fig.add_subplot(1, 1, 1)

plt.set_ylim(0, 100)
plt.set_xlim(0, len(curr_sensor["x_vals"]))
# naming the x axis
plt.set_xlabel('Reading Times')
# naming the y axis
plt.set_ylabel('Sensor Levels')

# giving a title to my graph
plt.set_title('Sensor data for %s' % curr_sensor["name"])

plt.plot(curr_sensor["x_vals"], curr_sensor["y_vals"], color='green', linestyle='dashed',
         linewidth=3, marker='o', markerfacecolor='blue', markersize=12)

# Convert plot to PNG image
pngImage = io.BytesIO()
FigureCanvas(fig).print_png(pngImage)

pngImageB64String = "data:image/png;base64,"
pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

curr_sensor["image"] = pngImageB64String'''