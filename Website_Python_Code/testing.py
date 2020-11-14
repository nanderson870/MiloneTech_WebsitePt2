from flask_website.dbAPI import accounts
import flask_bcrypt as bcrypt
from flask_website.dbAPI import sensors
from flask_website.dbAPI import sensor_readings
from pprint import pprint

if __name__ == '__main__':

    sensors.set_sensor_group('101',"Testing Group")

'''    for i in range (0,10):
        sensor_readings.add_reading_no_time(202, 50 - (i * 2), 40, 0)'''

