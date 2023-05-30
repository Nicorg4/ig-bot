from flask import Flask
from controllers.OperatorController import operator_blueprint
from controllers.igAccountController import igAccount_blueprint
from controllers.DestinationController import destination_blueprint
from controllers.DestinationParamsController import destinationParams_blueprint
from controllers.CycleController import cycle_blueprint
from flask_sqlalchemy import SQLAlchemy
from database.db_config import DATABASE_URL
from database.db_session import db_session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(operator_blueprint)
app.register_blueprint(igAccount_blueprint)
app.register_blueprint(destination_blueprint)
app.register_blueprint(destinationParams_blueprint)
app.register_blueprint(cycle_blueprint)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, port=8000)