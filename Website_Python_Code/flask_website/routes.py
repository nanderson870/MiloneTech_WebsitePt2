from flask import render_template, url_for, flash, redirect, Response, request
'''from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import figure
'''
import datetime
import io
import base64
import json
from flask_website.forms import RegistrationForm, LoginForm, SettingsForm, AccountForm, SensorAccountForm
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
    data_string = data_string + str(request.json) + "\n"

    with open('./flask_website/records.txt', 'a') as f:
        f.write(data_string)


    '''
    sensor_msg = request.json
    db.sensor_readings.add_reading_no_time(sensor_msg["Sensor ID"], sensor_msg["Liquid %"], sensor_msg["Battery %"], 0)
    '''
    return "OK"

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    sensorAccountForm=SensorAccountForm()
    if form.validate_on_submit():
        if form.newEmail.data != '':
            db.accounts.set_account_email(current_user.email, form.newEmail.data)
            flash('email updated', 'success')
        if form.phoneNumber.data != '':
            db.accounts.set_account_phone(current_user.email, form.phoneNumber.data)
            flash('phone number updated', 'success')
        if form.password.data != '':
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if form.password.data == form.confirmPassword.data:
                db.accounts.set_account_password(hashed_pass, current_user.email)
                flash('password updated', 'success')
    else:
        flash('button not pressed', 'danger')
    if sensorAccountForm.validate_on_submit():
        if sensorAccountForm.sensorID.data != '':
            flash('sensor ID: ' + sensorAccountForm.sensorID.data + ' has been added to your account', 'success')
            db.sensors.add_sensor_to_account(sensorAccountForm.sensorID.data, current_user.email)
            db.accounts.set_account_payment_tier(0, current_user.email)
    return render_template('account.html', title='Account', form=form, sensorAccountForm=sensorAccountForm, account_info=current_user.user_data)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
        flash(db.sensors.get_sensor_info(6767), 'success')
        flash(db.accounts.get_id_by_email(current_user.email), 'success')
        flash(db.alerts.check_alerts(541, 6767), 'success')
        form = SettingsForm()
        form.sensorID.choices = [('my', db.sensors.get_all_sensors(db.accounts.get_id_by_email(current_user.email)[0])[0])]
        if form.validate_on_submit():
            flash('here', 'success')
            "db.alerts.add_sensor_alert(db.accounts.get_id_by_email(current_user.email)[0], 6767, '50%', 'e', null)"
            db.sensors.set_sensor_name(6767, form.newSensorName)
            flash('here', 'success')
        else:
            flash('failed validate on submit', 'danger')
        return render_template('settings.html', title='Settings', form=form, account_info=current_user.user_data)

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
