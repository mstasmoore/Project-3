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

@app.route("/graphs")
def graphs():
    return render_template("graphs.html")
# API

@app.route("/api/paranormal/activityType/table/<activity_type>")
def paranormal_byType_table(activity_type):
    session = Session(engine)
    results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude, \
            paranormal_activity.encounter_seconds, paranormal_activity.season, paranormal_activity.image).filter(paranormal_activity.type == activity_type).limit(500).all() 
    results = [list(r) for r in results]
    table_results = {
        "table": results
    }
    session.close()
    return jsonify(table_results)

@app.route("/api/paranormal/activityType/<activity_type>")
def paranormal_byType(activity_type):
    
    session = Session(engine)
    
    pactivity_byType = [] 
    if activity_type != 'All':
        results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == activity_type).limit(500).all()
        addRecords(results, pactivity_byType)
    else:
        results1 = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == 'Amazing').limit(500).all()
        addRecords(results1, pactivity_byType)
        results2 = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == 'Big foot').limit(500).all()
        addRecords(results2, pactivity_byType)
        results3 = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == 'Haunted').limit(500).all()
        addRecords(results3, pactivity_byType)
        results4 = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.type, paranormal_activity.country, paranormal_activity.latitude, paranormal_activity.longitude,\
              paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == 'UFO').limit(500).all()
        addRecords(results4, pactivity_byType)

    session.close()
   
    return jsonify(pactivity_byType)

def addRecords(results, resultsDictionary):
    for description, city, state, type, country, latitude, longitude, encounter_seconds, season in results:
        new_dict = {}
        new_dict["Title"] = description
        new_dict["City"] = city
        new_dict["State"] = state
        new_dict["Type"] = type
        new_dict["Country"] = country
        new_dict["Latitude"] = latitude
        new_dict["Longitude"] = longitude
        new_dict["Seconds"] = encounter_seconds
        new_dict["Season"] = season
        resultsDictionary.append(new_dict)
    return resultsDictionary

@app.route("/api/paranormal/totals")
def paranormal_Totals():
    session = Session(engine)
    results = session.query(paranormal_activity.type, func.count(paranormal_activity.id)).group_by(paranormal_activity.type).all()
    print(results)
    session.close()

    pactivityLabels = []
    pactivityTotals = []
    for type, count in results:
        pactivityLabels.append(type)
        pactivityTotals.append(count)

    paranormal_results = {
        "Labels": pactivityLabels,
        "Totals": pactivityTotals,
    }

    return jsonify(paranormal_results)
    
if __name__ == "__main__":
    app.run(debug=True)
