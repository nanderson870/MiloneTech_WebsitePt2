from sqlalchemy.orm import scoped_session, sessionmaker
import Website_Python_Code.flask_website.dbAPI.accounts as accounts
import Website_Python_Code.flask_website.dbAPI.sensors as sensors
import Website_Python_Code.flask_website.dbAPI.sensor_readings as sensor_readings
import Website_Python_Code.flask_website.dbAPI.alerts as alerts
from . import alerts, db


if __name__ == '__main__':
    db_session = scoped_session(sessionmaker(bind=db.engine))
    print('beep')

    print(alerts.check_alerts(1, '100.101'))
