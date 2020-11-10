from flask_website.dbAPI import accounts
import flask_bcrypt as bcrypt
from flask_website.dbAPI import sensors
from flask_website.dbAPI import sensor_readings

if __name__ == '__main__':

    sensors.add_sensor_to_account("1","lucasgrebe@gmail.com")
