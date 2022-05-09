from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from weather_api_service.config import *
from weather_api_service.utils import *

app = Flask(__name__)
app.config.update(app_config_dict)
CORS(app)
app.app_context().push()

db = SQLAlchemy(app)
db.init_app(app)

from weather_api_service.models.User import User as UserModel

from weather_api_service.routes import User
from weather_api_service.routes import Countries
from weather_api_service.routes.Countries import app_countries
from weather_api_service.routes.User import app_user
from weather_api_service.routes.Weather import app_weather
from weather_api_service.routes.Analytics import app_analytics

with app.app_context():
    db.create_all()

print('Adding Users')
try:
    import csv

    file = './data/username.csv'
    dict_from_csv = {}

    with open(file, mode='r') as infile:
        reader = csv.reader(infile)
        for i, line in enumerate(reader):
            if i != 0:
                try:
                    row = list(line)
                    enc_pass = encrypt(secret_key=secret_key, plain_text=row[2])
                    user = UserModel(username=row[1], password=enc_pass, full_name=row[3], role=row[4])
                    db.session.add(user)
                    db.session.commit()
                    print('User Added: ' + row[3])
                except Exception as e:
                    print('Exception occurred while loading users: ' + str(e))
                    print('Rolling back...')
                    db.session.rollback()
except Exception as e:
    print('Exception occurred while loading users: ' + str(e))
    pass


@app.route('/')
def ping():  # put application's code here
    return 'pong'

if __name__ == "__main__":
    app.register_blueprint(app_countries)
    app.register_blueprint(app_user)
    app.register_blueprint(app_weather)
    app.register_blueprint(app_analytics)
    app.run()
