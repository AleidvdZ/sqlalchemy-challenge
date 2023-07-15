# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

#Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)

# #################################################
# # Flask Routes
# #################################################

# Home page
@app.route("/")
def welcome():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

    session.close()

# API static routes
# Preciptiation route
@app.route("/api/v1.0/precipitation")
def preciptiation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return json of date and preciptiation"""
    # Convert the query results from your precipitation analysis (only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    query_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_ago).\
        order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list 
    precip = list(np.ravel(results))
    
    # Return the JSON representation of your dictionary.
    return jsonify(precip)

# Stations route
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return json of stations"""
    # station_results = session.query(measurement.station).distinct()
    station_results = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Convert list of tuples into normal list 
    stations = list(np.ravel(station_results))

    # Return a JSON list of stations from the dataset.
    return jsonify(stations)

# temp route
@app.route("/api/v1.0/tobs")
def temperature():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return json for the last year recorded for most active station"""
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    year_ago2 = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    results2 = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= year_ago2).\
        filter(measurement.station == 'USC00519281').\
        order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list 
    temperature = list(np.ravel(results2))

    #Return a JSON list of temperature observations for the previous year.
    return jsonify(temperature)

# API dynamic route
@app.route("/api/v1.0/<start>")
def temp_start():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a json list of the min temp, ave temp, max temp for a specified start or start-end range."""
    # Return 

#   #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# @app.route("/api/v1.0/<start>/<end>")
# def temp_start_end():

#     """Return.."""
#      #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

# session.close()

if __name__ == '__main__':
    app.run(debug=True)

