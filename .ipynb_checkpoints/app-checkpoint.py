# Import neccessary libraries to build a server
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data

app = Flask(__name__)

# PyMongo connection setup
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

# Create route to query MongoDB
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)


# create a route call scrape
@app.route("/scrape")
def scrape():
    # run the scrape function
    web_data = scrape_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, web_data, upsert=True)

    # Redirect back to home page
    # return redirect("/", code = 302) #302 is default
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
