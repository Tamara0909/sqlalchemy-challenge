# Python SQL toolkit and Object Relational Mapper
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False})
# reflect an existing database into a new model
automap = automap_base()
# reflect the tables
automap.prepare (engine, reflect=True)
# View all of the classes that automap found
automap.classes.keys()
# Save references to each table
Measurement = automap.classes.measurement
Station = automap.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/")
def index():
    return """
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/<start><br/>
    /api/v1.0/<start>/<end>
    """
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Find the most recent date in the data set.
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date
    average_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365))).all()
    precipitation_dict = {date: prcp for date, prcp in average_precipitation}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations_list = session.query(Station.station).all()
    stations_list = list(np.ravel(stations_list))
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs(): 
    station_temperature = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365))).all()
    station_temperature = list(np.ravel(station_temperature))
    return jsonify(station_temperature)

@app.route("/api/v1.0/<start>") 
@app.route("/api/v1.0/<start>/<end>")
def start(start = None, end = None):
    results = []
    if not end:
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()       
    else:
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()       
    stats = list(np.ravel(results))
    return jsonify(stats)



if __name__ == '__main__':
    app.run()
