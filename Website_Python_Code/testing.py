from flask_website.dbAPI import accounts
import flask_bcrypt as bcrypt
from flask_website.dbAPI import sensors
from flask_website.dbAPI import sensor_readings
from pprint import pprint

if __name__ == '__main__':

    "0004A30B00F1DA7A"
    print(sensors.get_acc_id_by_sens_id('0004A30B00F1DA7A'))

'''    for i in range (0,10):
        sensor_readings.add_reading_no_time(202, 50 - (i * 2), 40, 0)'''

