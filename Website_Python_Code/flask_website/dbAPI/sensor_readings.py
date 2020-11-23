from sqlalchemy import exc
from . import db
from . import sensors


class SensorReadings(db.Base):
    __table__ = db.Base.metadata.tables['sensor_readings']


def add_reading_no_time(sens_id, liquid, battery, rssi):
    try:
        with db.engine.connect() as connection:
            connection.execute("insert into sensor_readings "
                               "values (default, {}, '{}', {}, {}, default, {})"
                               .format(sensors.get_acc_id_by_sens_id(sens_id), sens_id, liquid, battery, rssi))
            return True
    except exc.SQLAlchemyError:
        return False


def add_reading_yes_time(sens_id, liquid, battery, time_stamp, rssi):
    try:
        with db.engine.connect() as connection:
            connection.execute("insert into sensor_readings "
                               "values (default, {}, '{}', {}, {}, {}, {})"
                               .format(sensors.get_acc_id_by_sens_id(sens_id), sens_id, liquid, battery, time_stamp, rssi))
            return True
    except exc.SQLAlchemyError:
        return False


def get_sensor_data_points(sens_id):
    try:
        with db.engine.connect() as connection:
            data = []
            result = connection.execute("select * "
                                        "from sensor_readings "
                                        "where sensorID = '{}'"
                                        .format(sens_id))
            for row in result:
                data.append(row)
            return data
    except exc.SQLAlchemyError:
        return False


def get_sensor_battery(sens_id):
    try:
        with db.engine.connect() as connection:
            battery = ""
            result = connection.execute("select batteryLevel "
                                        "from sensor_readings "
                                        "where sensorID = '{}' "
                                        "order by recordNumber "
                                        "desc limit 1"
                                        .format(sens_id))
            for row in result:
                battery = row['batteryLevel']
            return battery
    except exc.SQLAlchemyError:
        return False


def get_liquid_level(sens_id):
    try:
        with db.engine.connect() as connection:
            liquid = 0
            result = connection.execute("select liquidLevel "
                                        "from sensor_readings "
                                        "where sensorID = '{}' "
                                        "order by recordNumber "
                                        "desc limit 1".format(sens_id))
            for row in result:
                liquid = row['liquidLevel']
            return liquid
    except exc.SQLAlchemyError:
        return False
