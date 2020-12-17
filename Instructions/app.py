from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 
from markupsafe import Markup

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db" 
mongo = PyMongo(app)

@app.route("/")
def  function_one():
    context = mongo.db.news_title.find_one()
    print(context)
    table = Markup(context["m_facts"])
    # news_title = {"Title": "Fake Title"}
    # news_data = scrape_mars.scrape1()
    # content_dict = {
    #     "hood": news_data["news_p"],
    #     "test": "hello world"
    # }
    # print(news_data)
    # print(content_dict)
    return render_template("index.html", context=context, table=table)

    

@app.route("/scrape")
def scraper():
    news_title = mongo.db.news_title
    news_title_data = scrape_mars.scrape()
    news_title.delete_many({})
    news_title.insert_one(news_title_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


# def function-two():


    