from sqlalchemy import exc
import flask_website.dbAPI.db as db


class SensorReadings(db.Base):
    __table__ = db.Base.metadata.tables['sensor_readings']


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
