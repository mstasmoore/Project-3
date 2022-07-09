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
print(Base.classes.keys())

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

@app.route("/analysis")
def dataAnalysis():
    return render_template("analysis.html")

@app.route("/data")
def data():
    return render_template("data.html")
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

@app.route("/api/paranormal/<country>")
def paranormal_byCountry(country):
    session = Session(engine)
    results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.type, paranormal_activity.latitude, paranormal_activity.longitude).filter(paranormal_activity.country == country).limit(50).all()
    #print(results)
    session.close()

    pactivity_byCountry = []
    for description, city, state, type, latitude, longitude in results:
        new_dict = {}
        print(city)
        #print(type)
        #print(latitude)
        #print(longitude)
        #new_dict["Title"] = description

        #new_dict["Type"] = type
        #new_dict["Latitude"] = latitude
        #new_dict["Longitude"] = longitude
        pactivity_byCountry.append(new_dict)
    return jsonify(pactivity_byCountry)

@app.route("/api/paranormal/<type>")
def paranormal_byType(activity_type):
    session = Session(engine)
    results = session.query(paranormal_activity.description, paranormal_activity.city, paranormal_activity.state, paranormal_activity.country, paranormal_activity.date, paranormal_activity.latitude, paranormal_activity.longitude,
    paranormal_activity.encounter_seconds, paranormal_activity.season).filter(paranormal_activity.type == activity_type).all()

    session.close()
    pactivity_byType = []
    for description, type, latitude, longitude in results:
        new_dict = {}
        new_dict["Title"] = description
        new_dict["Type"] = type
        new_dict["Latitude"] = latitude
        new_dict["Longitude"] = longitude
        pactivity_byType.append(new_dict)
    return jsonify(pactivity_byType)


@app.route("/api/directors/<director>")
def directors(director):

    print(director)

    if director == "chaplin":
        name = "Charles Chaplin"
    elif director == "hitchcock":
        name = "Alfred Hitchcock"
    elif director == "nolan":
        name = "Christopher Nolan"
    else:
        name = "Akira Kurosawa"

    session = Session(engine)

    G_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="G").filter(Movies.director == name).all()
    PG_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="PG").filter(Movies.director == name).all()
    PG_plus_results = session.query(func.avg(Movies.imdb_score)).filter(or_(Movies.rating=="PG+", Movies.rating=="PG-13")).filter(Movies.director == name).all()
    R_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="R").filter(Movies.director == name).all()
    Other_results = session.query(func.avg(Movies.imdb_score)).filter(or_(Movies.rating=="APPROVED",Movies.rating=="NOT RATED", Movies.rating=="N\A", Movies.rating=="PASSED")).filter(Movies.director == name).all()

    results = [G_results[0][0], PG_results[0][0], PG_plus_results[0][0], R_results[0][0], Other_results[0][0]]
    labels = ["G", "PG", "PG+", "R", "Other"]

    director_results = {
        "labels": labels,
        "scores": results,
    }

    session.close()

    return jsonify(director_results)

if __name__ == "__main__":
    app.run(debug=True)
