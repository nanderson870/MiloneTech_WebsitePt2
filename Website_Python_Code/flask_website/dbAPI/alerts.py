from sqlalchemy import exc
from . import db


class Alerts(db.Base):
    __table__ = db.Base.metadata.tables['alerts']


def check_alerts(acc_id, sens_id):
    try:
        with db.engine.connect() as connection:
            checker = []
            result = connection.execute("select * "
                                        "from alerts "
                                        "where accountID = {} and sensorID = '{}'"
                                        .format(acc_id, sens_id))
            for row in result:
                checker.append(row)
            return checker
    except exc.SQLAlchemyError:
        return False


# add elif for more thorough checking. want to be able to have multiple alerts for different values of same accId/sensID
# right now it checks to see if there are currently no alerts for acc/sensor. if so add an alert, otherwise update
# existing alert to contain new alert details. need to be more specific in checking. potentially check if the trigger
# levels are the same. i'll do this soon 11/5/20
def add_sensor_alert(acc_id, sens_id, trigger, email_alert, phone_alert):
    try:
        with db.engine.connect() as connection:
            checker = check_alerts(acc_id, sens_id)
            if len(checker) == 0 or not checker:
                connection.execute(
                    "insert into alerts "
                    "values ({}, '{}', {}, {}, {})"
                    .format(acc_id, sens_id, trigger, email_alert, phone_alert))
                return True
            elif checker[2] == trigger and checker[3] == email_alert and checker[4] == phone_alert:
                return True
            else:
                connection.execute(
                    "update alerts "
                    "set alerts.triggerLevel = {}, alerts.alertEmail = {}, alerts.alertPhone = {} "
                    "where alerts.accountID = {} and alerts.sensorID = {}"
                    .format(trigger, email_alert, phone_alert, acc_id, sens_id))
                return True
    except exc.SQLAlchemyError:
        return False


def remove_alert(acc_id, sens_id):
    try:
        with db.engine.connect() as connection:
            connection.execute("delete from alerts "
                               "where accountID = {} and sensorID = '{}'"
                               .format(acc_id, sens_id))
            return True
    except exc.SQLAlchemyError:
        return False


def get_alert_type(acc_id, sens_id):
    try:
        with db.engine.connect() as connection:
            alert_type = []
            result = connection.execute(
                "select alertEmail, alertPhone "
                "from alerts "
                "where accountID = {} and sensorID = '{}'"
                .format(acc_id, sens_id))
            for row in result:
                alert_type.append(row)
            return alert_type[0]
    except exc.SQLAlchemyError:
        return False
