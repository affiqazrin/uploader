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

