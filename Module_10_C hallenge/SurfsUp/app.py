# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite').connect

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    return (
        "<h1 style='text-align: center; font-size: 36px;'>Welcome to the Climate App!</h1>"
        "<h2><a href='/api/v1.0/precipitation' style='color: red;'>Precipitation</a></h2>"
        "<h2><a href='/api/v1.0/stations' style='color: red;'>Stations</a></h2>"
        "<h2><a href='/api/v1.0/tobs' style='color: red;'>Tobs</a></h2>"
        "<h2><p style='color: green;'>Start date query</p></h2>"
        "<h5><p style='color: green;'>example: /api/v1.0/start?start=yyyy-mm-dd</p></h5>"
        "<h2><p style='color: green;'>Start & End date query</p></h2>"
        "<h5><p style='color: green;'>example: /api/v1.0/start_end?start=yyyy-mm-dd&end=yyyy-mm-dd</p></h5>"
    )

# Define routes for precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = datetime.strptime(most_recent_date.date, '%Y-%m-%d')

    # Calculate one year ago from the most recent date
    one_year_ago = datetime(most_recent_date.year - 1, most_recent_date.month, most_recent_date.day -1)

    # Query to retrieve the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .filter(Measurement.date <= most_recent_date)\
        .order_by(Measurement.date).all()
    
    # Create a dictionary from the query results
    precipitation_data ={}
    for date, prcp in results:
        precipitation_data[date]=prcp

    return jsonify(precipitation_data)

