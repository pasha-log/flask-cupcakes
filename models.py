"""Models for Cupcake app."""

"""Create Cupcake model in models.py.

It should have the following columns:

id: a unique primary key that is an auto-incrementing integer
flavor: a not-nullable text column
size: a not-nullable text column
rating: a not-nullable column that is a float
image: a non-nullable text column. If an image is not given, default to https://tinyurl.com/demo-cupcake
Make a database called cupcakes.
""" 

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy() 

def connect_db(app): 
    db.app = app 
    db.init_app(app) 

class Cupcake(db.Model): 
    """Cupcake Model""" 

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    flavor = db.Column(db.Text, nullable=False) 
    size = db.Column(db.Text, nullable=False) 
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default='https://tinyurl.com/demo-cupcake')

    def serialize(self): 
        return {
            'id': self.id, 
            'flavor': self.flavor, 
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }

    def __repr__(self): 
        return f"<Cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image}>" 