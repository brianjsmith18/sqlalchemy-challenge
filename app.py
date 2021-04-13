import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
session = Session(engine)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    p_list = []
    for x , y in results:
        p_dict = {}
        p_dict ["date"]= x
        p_dict ["prcp"]= y
        p_list.append(p_dict)
    return jsonify(p_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    
    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    # Return a JSON list of stations from the dataset.
    all_stations = []
    for station in stations:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    
    temp_results = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    # Return a JSON list of temperature observations (TOBS) for the previous year.

    temp_list = []
    for temps in temp_results:
        temps_dict = {}
        temps_dict["station"] = station
        temps_dict["tobs"] = temperatures
        temp_list.append(temps_dict)

    return jsonify(temp_list)


if __name__ == '__main__':
    app.run(debug=True)
