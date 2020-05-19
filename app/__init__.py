from flask import Flask, jsonify, json
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__) # initiate a flask instance
app.config.from_object(Config) # pass in configuration object defined in config.py
db = SQLAlchemy(app) # initiate a database object
migrate = Migrate(app, db) # initiate a "migrate" object
bootstrap = Bootstrap(app) 
moment = Moment(app) 

login = LoginManager(app) # initiate a log-in
login.login_view = 'login'

from app import routes, models, errors
import pandas as pd #for csv


df = pd.read_csv('spaces.csv', header=None)
# add all buildings from csv to database
for i in range(df.count()[0]):
    # see if building exists. if not, add new building to db.
    building = models.Building.query.filter_by(name = df[0][i]).first()
    # if not found, then create a new building
    if building is None:
        building = models.Building(name = df[0][i])
        db.session.add(building)

    # see if space exists. if not, add new space to db.
    space = models.StudySpace.query.filter_by(building_id=building.id).filter_by(name=df[1][i]).first()
    if space is None:
        space = models.StudySpace(name = df[1][i], building = building, lat = df[2][i], long = df[3][i])
        db.session.add(space)
db.session.commit()
