from sqlalchemy import exc
import Website_Python_Code.flask_website.dbAPI.db as db


class Sensors(db.Base):
    __table__ = db.Base.metadata.tables['sensors']


def add_sensor(acc_id, sens_id, sens_size, sens_type, name):
    try:
        with db.engine.connect() as connection:
            connection.execute("insert into sensors "
                               "values ({}, '{}', {}, '{}', '{}', default, null)"
                               .format(acc_id, sens_id, sens_size, sens_type, name))
            return True
    except exc.SQLAlchemyError:
        return False


# not 100 on this one
def add_sensor_to_account(sens_id, email):
    try:
        with db.engine.connect() as connection:
            connection.execute("update sensors "
                               "set sensors.accountID = (select accountID "
                                                        "from accounts "
                                                        "where accountEmail = '{}') "
                               "where sensorID = '{}'"
                               .format(email, sens_id))
            return True
    except exc.SQLAlchemyError:
        return False


def get_all_sensors(acc_id):
    try:
        with db.engine.connect() as connection:
            sens = []
            result = connection.execute("select sensorID "
                                        "from sensors "
                                        "where accountID = {}"
                                        .format(acc_id))
            for row in result:
                sens.append(row['sensorID'])
            return sens
    except exc.SQLAlchemyError:
        return False


def get_sensor_info(sens_id):
    try:
        with db.engine.connect() as connection:
            sens = []
            result = connection.execute("select * "
                                        "from sensors "
                                        "where sensorID = '{}'"
                                        .format(sens_id))
            for row in result:
                sens.append(row)
            return sens
    except exc.SQLAlchemyError:
        return False


def set_sensor_name(sens_id, sens_name):
    try:
        with db.engine.connect() as connection:
            connection.execute("update sensors "
                               "set sensorName = '{}' "
                               "where sensorID = '{}'"
                               .format(sens_name, sens_id))
            return True
    except exc.SQLAlchemyError:
        return False


def set_sensor_group(sens_id, sens_group):
    try:
        with db.engine.connect() as connection:
            connection.execute("update sensors "
                               "set sensorGroup = '{}' "
                               "where sensorID = '{}'"
                               .format(sens_group, sens_id))
            return True
    except exc.SQLAlchemyError:
        return False
