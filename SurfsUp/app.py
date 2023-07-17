# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import datetime

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

# Landing page
@app.route("/")
def welcome():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List all available api routes."""
    return (
        f"This page can be used to analyze weather data for weather stations around Honolulu, Hawaii<br/>"
        f"-------------------------------------------------------------------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<br/>"
        f"-------------------------------------------------------------------------------------------<br/>"
        f"(Note: for the last two routes use the date format of YYYY-MM-DD for the start and end dates)<end>"
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
def temp_start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a json list of the min temp, ave temp, max temp for a specified start or start-end range."""   
    start = datetime.strptime(start, '%Y-%m-%d').date()
 
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list and extract the values
    temp = list(np.ravel(results))
          
    min = temp[0]
    max = temp[1]
    avg = temp[2]

    # Return response for given start date
    try:
        return(
            f"For the start date ({start}) you selected to the most recent recording:<br/>"
            f"- the minimum temperature was {min} F<br/>"
            f"- the maximum temperature was {max} F<br/>"
            f"- the average temperature was {avg} F<end>"
        )

    except ValueError:
       raise ValueError('date is not valid date in the format YYYY-MM-DD'.format(start))


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a json list of the min temp, ave temp, max temp for a  start-end range."""   
    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()    

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list and extract the values
    temp = list(np.ravel(results))
          
    min = temp[0]
    max = temp[1]
    avg = temp[2]

    # Return response for given start-end date range
    try:
        return(
            f"For the date range ({start} through {end}) you selected:<br/>"
            f"- the minimum temperature was {min} F<br/>"
            f"- the maximum temperature was {max} F<br/>"
            f"- the average temperature was {avg} F<br/>"
        )

    except ValueError:
       raise ValueError('date is not valid date in the format YYYY-MM-DD'.format(start))

if __name__ == '__main__':
    app.run(debug=True)