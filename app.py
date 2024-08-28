from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# This is a mongodb database
db = client.flask_database

# This is a todos collection
todos = db.todos

if __name__ == "__main__":
    app.run(debug=True)
