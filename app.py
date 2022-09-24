"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, Cupcake
import os

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'bUFEHUWEF900')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app) 
db.create_all() 

@app.route('/') 
def index_page(): 
    """GET /
        This should return an HTML page (via render_template). 
        This page should be entirely static (the route should just render the template, without providing any information on cupcakes in the database).
        It should simply have an empty list where cupcakes should appear and a form where new cupcakes can be added.

        Write Javascript (using axios and jQuery) that:
        queries the API to get the cupcakes and adds to the page
        handles form submission to both let the API know about the new cupcake and updates the list on the page to show it
    """
    return render_template('index.html') 
    
@app.route('/api/cupcakes')
def all_cupcakes():
    """GET /api/cupcakes
        Get data about all cupcakes.

        Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.

        The values should come from each cupcake instance.
    """

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """GET /api/cupcakes/[cupcake-id]
        Get data about a single cupcake.

        Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

        This should raise a 404 if the cupcake cannot be found.
    """
    cupcake = Cupcake.query.get_or_404(id) 
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """POST /api/cupcakes
        Create a cupcake with flavor, size, rating and image data from the body of the request.

        Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    """
    # print(request.json)
    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """PATCH /api/cupcakes/[cupcake-id]
        Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. 
        You can always assume that the entire cupcake object will be passed to the backend.

        This should raise a 404 if the cupcake cannot be found.

        Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
    """
    data = request.json
    cupcake = Cupcake.query.get_or_404(id) 
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit() 

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """DELETE /api/cupcakes/[cupcake-id]
        This should raise a 404 if the cupcake cannot be found.

        Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.
    """
    cupcake = Cupcake.query.get_or_404(id) 
    db.session.delete(cupcake) 
    db.session.commit() 
    return jsonify(message="Deleted")





