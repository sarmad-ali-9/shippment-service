from flask                 import Flask
from sqlalchemy.engine.url import URL
from routes.vessel_routes  import vessel_bp
from routes.voyage_routes  import voyage_bp
from configparser          import ConfigParser
from models.models         import db
from logger.logger         import log

app    = Flask(__name__)
logger = log(__name__)

# Register vessel and voyage routes blueprint with the Flask Application
app.register_blueprint(vessel_bp)
app.register_blueprint(voyage_bp)

try:
    # Read port and debug toggle from config ini file
    try:
        config_ini = ConfigParser()
        config_ini.read('app.ini')

        port  = config_ini.getint('server', 'port')
        debug = config_ini.getboolean('server', 'debug')

    except Exception:
        logger.warning("Unable to read  port and debug toggle. Setting default values of 5000 and False")
        port  = 5000
        debug = False

    # Configure Flask Application with SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        database="shippments.db",
        drivername="sqlite"
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()

except Exception as e:
    logger.warning("Warning: {}".format(e))

if __name__ == '__main__':
    try:
        app.run(debug=debug, host='0.0.0.0', port=port)
    except Exception as e:
        logger.critical("Unable to start flask application")
        logger.critical(e)
