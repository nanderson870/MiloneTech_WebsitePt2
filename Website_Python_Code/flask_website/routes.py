from flask import render_template, url_for, flash, redirect, Response, request
'''from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import figure
'''
import datetime
import io
import base64
import json

import flask_website.emailer as email
from flask_website.forms import RegistrationForm, LoginForm, SettingsForm, AccountForm, SensorAccountForm,RequestResetForm, ResetPasswordForm
from flask_website import app, bcrypt, db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
import datetime
from pprint import pprint

class User(UserMixin):

    def initialize_user_data(self):

        # Getting Sensors for Account
        data = {}

        data["email"] = self.email
        data["payment_tier"] = db.accounts.get_status_by_id(self.id)

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

                print(sensor_data)

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

                    dateSQL = data_point[5]
                    dateSQL = dateSQL - datetime.timedelta(hours = 5)
                    date = str(dateSQL)

                    curr_sensor["x_vals"].append(date)

                    curr_sensor["y_vals"].append(data_point[3])
                    counter = counter + 1

                data["sensor_data"][group][sensor] = curr_sensor

        self.user_data = data

    def get_reset_token(self, expires_sec=1800):

        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps( { 'user_id':self.id }).decode('utf-8')

    def verify_reset_token(token):

        s = Serializer(app.config["SECRET_KEY"])

        try:
           user_id = s.loads(token)['user_id']
        except:
            return None

        return user_id


    def __init__(self, userID):
        self.id = userID
        self.email = db.accounts.get_email_by_id(userID)
        self.user_data = None



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

        userID = db.accounts.get_id_by_email(form.email.data)
        user = User(userID)


        if user and bcrypt.check_password_hash( db.accounts.get_pass_by_id(userID), form.password.data):

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

    current_user.initialize_user_data()

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

@app.route("/sensor", methods=['POST'])
def sensor():

    data_string = "Recieved post at: %s\n" % datetime.datetime.now()
    print(data_string)
    data = request.json
    data_string = data_string + str(data)


    with open('./flask_website/records.txt', 'a') as f:
        f.write(data_string)

    sensorID = data["Sensor ID"]

    '''all assuming that the sensor already exists in the DB'''
    curr_sensor_info = db.sensors.get_sensor_info(sensorID)

    if curr_sensor_info and curr_sensor_info[0][0] is not None:

        sensor_name = curr_sensor_info[0][4]

        #if the sensor_name is Null in DB, just make it equal to the sensorID
        if not sensor_name:
            sensor_name = sensorID

        owner_acc_info = db.accounts.get_all_by_id(curr_sensor_info[0][0])
        '''owner_acc_info structure FOR NOW
        (acc_id, 'acc_email', fname , lname, number, pass_hash, is_paid)'''

        curr_sensor_alerts = db.alerts.check_alerts(sensorID)
        '''curr_sensor_alerts structure FOR NOW
        [(rec num,acc_id, 'sens_id', trig_lev , email? (0/1/2), text? (0/1/2))]'''

        for poss_alert in curr_sensor_alerts:

            for entry in data["Sensor Data"]:

                email_alert_enc = poss_alert[4]
                text_alert_enc = poss_alert[5]
                hit = False

                if entry["Liquid %"] >= poss_alert[3]:

                    '''(to_email, sensor, curr_user_name, alert_level, curr_level):'''
                    if email_alert_enc == 2:
                        email_alert_enc = 1
                        hit = True
                        pass

                    if  text_alert_enc == 2:
                        text_alert_enc = 1
                        hit = True
                        pass

                    if hit:
                        db.alerts.set_alert_type(poss_alert[0], email_alert_enc, text_alert_enc)
                        break


        #Code for sending out an email if the level is un-triggered
        for poss_alert in curr_sensor_alerts:

            for entry in data["Sensor Data"]:

                email_alert_enc = poss_alert[4]
                text_alert_enc = poss_alert[5]
                hit = False

                if entry["Liquid %"] < poss_alert[3]:

                    '''(to_email, sensor, curr_user_name, alert_level, curr_level):'''
                    if email_alert_enc == 1:
                        full_name = owner_acc_info[2] + " " + owner_acc_info[3]
                        email.send_email_notification(owner_acc_info[1],sensor_name, full_name ,poss_alert[3],entry["Liquid %"])
                        email_alert_enc += 1
                        hit = True
                        pass

                    if  text_alert_enc == 1:
                        #CODE FOR SENDING AN TEXT
                        text_alert_enc += 1
                        hit = True
                        pass

                    if hit:
                        db.alerts.set_alert_type(poss_alert[0], email_alert_enc, text_alert_enc)
                        break

    else:
        #the sensor doesn't exist in the db... create it
        # (TODO) FOR NOW with default values
        db.sensors.add_sensor(sensorID)



    for entry in data["Sensor Data"]:
        db.sensor_readings.add_reading_no_time(sensorID, entry["Liquid %"], entry["Battery %"],
                                               entry["RSSI"])

    time_response = str(db.sensors.get_sensor_time_between(sensorID)[0])
    print(time_response)
    print(type(time_response))

    return time_response


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
        db.sensors.add_sensor(541, 6868, 100, 'toxic', 'bobby')
        flash(db.sensors.get_sensor_info(6767), 'success')
        flash(db.alerts.check_alerts(current_user.id, 6767), 'success')
        flash(db.sensors.get_all_sensors(current_user.id), 'success')
        form = SettingsForm()
        for sensor in db.sensors.get_all_sensors(current_user.id):
                form.sensorID.choices.append((sensor, sensor))
                form.allTriggerValues.choices.append((db.alerts.check_alerts(current_user.id, sensor), db.alerts.check_alerts(current_user.id, sensor)))
        flash(form.allTriggerValues, 'success')
        if form.is_submitted():
            flash(form.textOrEmail.data, 'success')
            if form.textOrEmail.data == 1:
                db.alerts.add_sensor_alert(current_user.id, form.sensorID.data, form.level.data, 1, 0)
            else:
                db.alerts.add_sensor_alert(current_user.id, form.sensorID.data, form.level.data, 0, 1)
            db.sensors.set_sensor_name(6767, form.newSensorName)
            flash(form.sensorID.data, 'success')
        else:
            flash('no submit yet', 'danger')
        flash(current_user.user_data, 'danger')
        return render_template('settings.html', title='Settings', form=form, account_info=current_user.user_data)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

    form = RequestResetForm()

    if form.validate_on_submit():
        user = db.accounts.get_id_by_email(form.email.data)
        flash('An email has been sent with instructions on how to reset your password')
        user_obj = User(user)
        token = User.get_reset_token(user_obj)
        email.send_password_request(form.email.data, url_for('reset_token',token=token, _external=True))

        return redirect(url_for('login'))


    return render_template('reset_request.html', title = "Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    user = load_user(User.verify_reset_token(token))

    if user is None:
        flash('That is an Invalid/Expired Token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.accounts.set_account_password(hashed_pass, user.email )

        flash(f'Your password has been updated! You may now Login', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title = "Reset Password", form=form)

