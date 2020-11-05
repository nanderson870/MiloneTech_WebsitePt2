from sqlalchemy import exc
import Website_Python_Code.flask_website.dbAPI.db as db


class Alerts(db.Base):
    __table__ = db.Base.metadata.tables['alerts']


def check_alerts(acc_id, sens_id):
    try:
        with db.engine.connect() as connection:
            existing_alerts = []
            result = connection.execute("select * "
                                        "from alerts "
                                        "where accountID = {} and sensorID = '{}'"
                                        .format(acc_id, sens_id))
            for row in result:
                existing_alerts.append(row)
            return existing_alerts
    except exc.SQLAlchemyError:
        return False


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