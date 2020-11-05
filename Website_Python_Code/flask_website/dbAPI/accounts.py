from sqlalchemy import exc
import Website_Python_Code.flask_website.dbAPI.db as db


class Accounts(db.Base):
    __table__ = db.Base.metadata.tables['accounts']


def get_id_by_email(acc_email):
    with db.engine.connect() as connection:
        acc_id = []
        result = connection.execute("select accountID "
                                    "from accounts "
                                    "where accountEmail = '{}'"
                                    .format(acc_email))
        for row in result:
            acc_id.append(row[acc_id])
        return acc_id


def get_email_by_id(account_id):
    with db.engine.connect() as connection:
        email = []
        result = connection.execute("select accountEmail "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            email.append(row['accountEmail'])
    return email


def get_phone_by_id(account_id):
    with db.engine.connect() as connection:
        phone = []
        result = connection.execute("select phoneNumber "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            phone.append(row['phoneNumber'])
    return phone


def get_name_by_id(account_id):
    with db.engine.connect() as connection:
        name = []
        result = connection.execute("select fname, lname "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            name.append((row['fname'], row['lname']))
    return name


def get_pass_by_id(account_id):
    with db.engine.connect() as connection:
        pass_hash = []
        result = connection.execute("select passwordHash "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            pass_hash.append(row['passwordHash'])
    return pass_hash


def get_status_by_id(account_id):
    with db.engine.connect() as connection:
        account_status = []
        result = connection.execute("select accountStatus "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            account_status.append(row['accountStatus'])
    return account_status


'''
    Quick work around made by Isaac.
'''


def get_id_by_email(account_id):
    with db.engine.connect() as connection:
        account_status = []
        result = connection.execute("select accountEmail "
                                    "from accounts "
                                    "where accountID = {}"
                                    .format(account_id))
        for row in result:
            account_status.append(row['accountStatus'])
    return account_status


def create_account(email, first_name, last_name, pass_hash):
    try:
        with db.engine.connect() as connection:
            connection.execute("insert into accounts "
                               "values (default, '{}', '{}', '{}', null, '{}', 0)"
                               .format(email, first_name, last_name, pass_hash))
            return True
    except exc.SQLAlchemyError:
        return False


def set_account_email(old_email, new_email):
    try:
        with db.engine.connect() as connection:
            connection.execute("update accounts "
                               "set accountEmail = '{}' "
                               "where accountEmail = '{}'"
                               .format(new_email, old_email))
            return True
    except exc.SQLAlchemyError:
        return False


def set_account_password(pass_hash, email):
    try:
        with db.engine.connect() as connection:
            connection.execute("update accounts "
                               "set passwordHash = '{}' "
                               "where accountEmail = '{}'"
                               .format(pass_hash, email))
            return True
    except exc.SQLAlchemyError:
        return False


def set_account_payment_tier(status, email):
    try:
        with db.engine.connect() as connection:
            connection.execute("update accounts "
                               "set accountStatus = {} "
                               "where accountEmail = '{}'"
                               .format(status, email))
            return True
    except exc.SQLAlchemyError:
        return False


def set_account_phone(phone, email):
    try:
        with db.engine.connect() as connection:
            connection.execute("update accounts "
                               "set phoneNumber = '{}' "
                               "where accountEmail = '{}'"
                               .format(phone, email))
            return True
    except exc.SQLAlchemyError:
        return False
