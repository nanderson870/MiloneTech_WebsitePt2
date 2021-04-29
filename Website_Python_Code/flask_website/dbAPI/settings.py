# For storing and retrieving user settings. Currently only used for sensor measurement settings

from sqlalchemy import exc
from . import db


class Sensors(db.Base):
    __table__ = db.Base.metadata.tables['sensor_settings']


def has_stored_settings(sensor_id):
    try:
        with db.engine.connect() as connection:
            result = connection.execute("select * from sensor_settings "
                                        "where sensorID= '{}'"
                                        .format(sensor_id))
            data = []
            for row in result:
                data.append(row)
        return len(data) > 0
    except exc.SQLAlchemyError:
        return False


def get_sensor_settings(sensor_id):
    try:
        with db.engine.connect() as connection:
            result = connection.execute("select * from sensor_settings "
                                        "where sensorID='{}'"
                                        .format(sensor_id))
            data = []
            for row in result:
                data.append(row)
            return data[0]
    except exc.SQLAlchemyError as e:
        print(str(e))
        return False


def store_sensor_settings(new_settings):
    try:
        # This function inserts, so just redirect it to update_sensor_settings if there are already
        #   settings to ensure no duplicate entries
        if has_stored_settings(new_settings[0]):
            return update_sensor_settings(new_settings)

        # I assort the input into nicely named variables here, so that it's readable, and more
        #   importantly so that it throws an exception if the input doesn't have the right number of elements.
        sensor_id = new_settings[0]
        measurement_type = new_settings[1]
        width = new_settings[2]
        length = new_settings[3]
        radius = new_settings[4]
        height = new_settings[5]
        sensor_bottom_height = new_settings[6]
        sensor_top_height = new_settings[7]
        with db.engine.connect() as connection:
            result = connection.execute("insert into sensor_settings "
                                        "values ('{}', '{}', {}, {}, {}, "
                                        "{}, {}, {})"
                                        .format(sensor_id, measurement_type, width, length, radius,
                                                height, sensor_bottom_height, sensor_top_height))
        return True
    except exc.SQLAlchemyError as e:
        print(str(e))
        return False


def update_sensor_settings(new_settings):
    try:
        sensor_id = new_settings[0]
        measurement_type = new_settings[1]
        width = new_settings[2]
        length = new_settings[3]
        radius = new_settings[4]
        height = new_settings[5]
        sensor_bottom_height = new_settings[6]
        sensor_top_height = new_settings[7]
        with db.engine.connect() as connection:
            result = connection.execute("update sensor_settings "
                                        "set "
                                        "measurementType = '{}', "
                                        "width = {}, "
                                        "length = {}, "
                                        "radius = {}, "
                                        "height = {}, "
                                        "sensorBottomHeight = {}, "
                                        "sensorTopHeight = {} "
                                        "where sensorID = '{}'"
                                        .format(measurement_type, width, length, radius,
                                                height, sensor_bottom_height, sensor_top_height, sensor_id))
            return True
    except exc.SQLAlchemyError as e:
        print(str(e))
        return False
