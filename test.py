if __name__ == '__main__':
    with app.app_context():
        app.secret_key = app.config['SECRET_KEY']

        # Check if the database is connected successfully
        try:
            db.create_all()
            print("Database connected successfully!")
        except Exception as e:
            app.logger.error(f"Error connecting to the database: {e}")

    app.run(debug=True,host='0.0.0.0', port=8888)




if __name__ == '__main__':
    app_config = config['default']  # Use the default configuration for now, you can choose the appropriate one
    app.config.from_object(app_config)

    with app.app_context():
        # Use the configured secret key
        app.secret_key = app.config['SECRET_KEY']



app = Flask(__name__)



app=Flask(__name__)
app.config['UPLOAD_FOLDER']='INC_STATEMENT'
app.config.from_object('config.ProductionConfig')  # Change to 'config.ProductionConfig' for production
#app.config['_external_route_base'] = True


# Load configuration from config.py
#app.config.from_pyfile('config.py')

# Initialize the SQLAlchemy extension
db=SQLAlchemy(app)

        # Check if the database is connected successfully
        try:
            initialize_database()
            print("Database connected successfully!")
            # Run the application only if the database connection is successful
            app.run(debug=True, host='0.0.0.0', port=8888)
        except Exception as e:
            app.logger.error(f"Error connecting to the database: {e}")



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'INC_STATEMENT'
app.config.from_object('config.ProductionConfig')  # Change to 'config.ProductionConfig' for production

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Assuming your config dictionary is defined in a module named config
from config import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'INC_STATEMENT'
app_config = config['default']  # Use the default configuration for now, you can choose the appropriate one
app.config.from_object(app_config)

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

if __name__ == '__main__':
    # Now you can use the initialized app and db objects as needed
    app.run(debug=True, host='0.0.0.0', port=8888)

def ldap_authenticate(username, password):
    try:
        server = Server(app.config['LDAP_SERVER'], get_info=ALL)
        conn = Connection(server, user=app.config['LDAP_BIND_USER'], password=app.config['LDAP_BIND_PASSWORD'], auto_bind=True)

        search_filter = f'(&(objectClass=person)(uid={username}))'
        conn.search(app.config['LDAP_SEARCH_BASE'], search_filter, attributes=['cn', 'uid'])

        if len(conn.entries) == 1:
            user_dn = conn.entries[0].entry_dn
            try:
                conn = Connection(server, user=user_dn, password=password, auto_bind=True)
                return True
            except LDAPExceptionError as e:
                # Handle the specific LDAPExceptionError for invalid password
                if 'Invalid credentials' in str(e):
                    return False
    except LDAPExceptionError:
        # Handle the general LDAPExceptionError for socket-related errors
        return False

    return False






from ldap3 import Server, Connection, ALL, LDAPExceptionError

# Define LDAP attribute constants
LDAP_CN_ATTRIBUTE = 'cn'
LDAP_UID_ATTRIBUTE = 'uid'

def ldap_authenticate(username, password):
    try:
        # Establish connection with LDAP server using service account
        server = Server(app.config['LDAP_SERVER'], get_info=ALL)
        service_account_conn = Connection(server, user=app.config['LDAP_BIND_USER'], password=app.config['LDAP_BIND_PASSWORD'], auto_bind=True)

        # Search for the user's entry
        search_filter = f'(&(objectClass=person)(uid={username}))'
        service_account_conn.search(app.config['LDAP_SEARCH_BASE'], search_filter, attributes=[LDAP_CN_ATTRIBUTE, LDAP_UID_ATTRIBUTE])

        if len(service_account_conn.entries) == 1:
            user_dn = service_account_conn.entries[0].entry_dn

            # Attempt user authentication
            try:
                user_conn = Connection(server, user=user_dn, password=password, auto_bind=True)
                return True
            except LDAPExceptionError as e:
                # Handle the specific LDAPExceptionError for invalid password
                if 'Invalid credentials' in str(e):
                    return False
        else:
            # Handle the case where user entry is not found
            return False

    except LDAPExceptionError as e:
        # Log the specific LDAPExceptionError details
        app.logger.error(f"LDAP authentication error: {e}")
        return False

    return False
