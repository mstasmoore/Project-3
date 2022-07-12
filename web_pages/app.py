# import necessary libraries
# from models import create_classes
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.automap import automap_base

import pickle

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

engine = create_engine("sqlite:///data/paranormal_activity.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
paranormal_activity = Base.classes.paranormal

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# ---------------------------------------------------------
# Web site
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maps")
def maps():
    return render_template("maps.html")

@app.route("/amazing")
def amazing():
    return render_template("amazing.html")

@app.route("/bigfoot")
def bigFoot():
    return render_template("bigfoot.html")

@app.route("/haunted")
def haunted():
    return render_template("haunted.html")

@app.route("/ufo")
def ufo():
    return render_template("ufo.html")

#@app.route("/assets/img/")
#def ufo():
#    return 
# ---------------------------------------------------------
# API
#@app.route("/api/movies")
#def movie_grid():

#    session = Session(engine)

#    results = session.query(Movies.title, Movies.director, Movies.year, Movies.rating, Movies.imdb_votes, Movies.imdb_score).all()

#    results = [list(r) for r in results]

#    table_results = {
#        "table": results
#    }

#    session.close()

#    return jsonify(table_results)

@app.route("/api/paranormal/country/<country>")
def paranormal_byCountry(country):
    session = Session(engine)
    results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.latitude, paranormal_activity.longitude, \
            paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.country == country).all()
    #print(results)
    session.close()

    pactivity_byCountry = []
    for description, city, state, type, latitude, longitude, encounter_seconds, season in results:
        new_dict = {}
        new_dict["Title"] = description
        new_dict["City"] = city
        new_dict["State"] = state
        new_dict["Type"] = type
        new_dict["Latitude"] = latitude
        new_dict["Longitude"] = longitude
        new_dict["Seconds"] = encounter_seconds
        new_dict["Season"] = season
        pactivity_byCountry.append(new_dict)
    return jsonify(pactivity_byCountry)

@app.route("/api/paranormal/activityType/<activity_type>")
def paranormal_byType(activity_type):
    print('Here')
    session = Session(engine)
    results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == activity_type).all()

    print(activity_type)
    print(results)
    session.close()
    pactivity_byType = []
    for description, city, state, country, latitude, longitude, encounter_seconds, season in results:
        new_dict = {}
        new_dict["Title"] = description
        new_dict["City"] = city
        new_dict["State"] = state
        new_dict["Country"] = country
        new_dict["Latitude"] = latitude
        new_dict["Longitude"] = longitude
        new_dict["Seconds"] = encounter_seconds
        new_dict["Season"] = season
        pactivity_byType.append(new_dict)
    return jsonify(pactivity_byType)


if __name__ == "__main__":
    app.run(debug=True)
