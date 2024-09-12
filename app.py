from flask import Flask, render_template, url_for, request, redirect, flash
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

try:
    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["flask_database"]

    # Connection attempt
    mydb.list_collection_names()
    print("MongoDB Connected")

    # Check if the database exists
    dblist = myclient.list_database_names()
    if "flask_database" in dblist:
        print("The database exists.")

except ConnectionFailure as e:
    print(f"Connection failed: {e}")

myCollection = mydb["todos"]

collectionList = mydb.list_collection_names()
if "todos" in collectionList:
    print("The collection exists also.")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        degree = request.form.get('degree')
        if content and degree:
            myCollection.insert_one({'content': content, 'degree': degree})
            return redirect(url_for('index'))  # Redirect after submission

    all_todos = myCollection.find()  # Fetch todos every time index is called
    return render_template('index.html', todos=all_todos)


@app.post("/<id>/delete")
def delete(id):
    myCollection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# New route to handle editing a todo
@app.route("/<id>/edit", methods=['POST'])
def edit(id):
    content = request.form.get('content')
    degree = request.form.get('degree')
    
    if content and degree:
        result = myCollection.update_one({"_id": ObjectId(id)}, {"$set": {'content': content, 'degree': degree}})
        if result.matched_count == 0:
            # Handle case where no document was found
            flash('Todo not found', 'error')
        else:
            flash('Todo updated successfully', 'success')
    else:
        flash('Content and degree are required', 'error')
    
    return redirect(url_for('index'))

# app.config['TEMPLATES_AUTO_RELOAD'] = True
if __name__ == "__main__":
    app.run(debug=True)