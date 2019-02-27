import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

# connect to mongo db 
mars_db_conn = client.mars_db
mars_data_collection = mars_db_conn.mars_data
@app.route('/')
def index():
    # finds db items and stores
    mars_list= list(mars_data_collection.find({}))
    # render an index.html template, pass in db data
    return render_template("index.html", mars_list=mars_list)

@app.route("/scrape")
def scraping():
    mars_data = scrape_mars.scrape()
    mars_data_collection.update({}, mars_data, upsert=True)
    print("Mars weather - ", mars_data['mars_weather'])
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)