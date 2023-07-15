# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

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

# Create our session (link) from Python to the DB
session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)

# #################################################
# # Flask Routes
# #################################################

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

# @app.route("/api/v1.0/precipitation")
# def preciptiation():
    
#     """Return.."""
#     #Convert the query results from your precipitation analysis (only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#     query_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    
#     year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
#     results = session.query(measurement.date, measurement.prcp).\
#         filter(measurement.date >= year_ago).\
#         order_by(measurement.date).all()
    
    
#     #Return the JSON representation of your dictionary.


# @app.route("/api/v1.0/stations")
# def stations():

#     """Return.."""
#     #Return a JSON list of stations from the dataset.


# @app.route("/api/v1.0/tobs")
# def temperature():

#     """Return.."""
#     #Query the dates and temperature observations of the most-active station for the previous year of data.

#     #Return a JSON list of temperature observations for the previous year.

# @app.route("/api/v1.0/<start>")
# def temp_start():

#     """Return.."""
#     #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#     #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# @app.route("/api/v1.0/<start>/<end>")
# def temp_start_end():

#     """Return.."""
#      #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

