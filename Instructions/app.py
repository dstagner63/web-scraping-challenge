from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db" 
mongo = PyMongo(app)

@app.route("/")
def  function_one():
    news_title = mongo.db.news_title.find_one()
    news_title = {"Title": "Fake Title"}
    news_data = scrape_mars.scrape1()
    content_dict = {
        "hood": news_data["news_p"],
        "test": "hello world"
    }
    print(news_data)
    print(content_dict)
    return render_template("index.html", title=news_data["news_title"], content=content_dict)

    

@app.route("/scrape")
def scraper():
    news_title = mongo.db.news_title
    news_title_data = scrape_mars_db.scrape()
    news_title.update({}, news_title_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


# def function-two():


    