'''' glitch dbs'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Glitch(db.Model):

    __tablename__ = "glitches"

    glitch_id   = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name        = db.Column(db.String(32), nullable=False) #name of glitch
    js_file     = db.Column(db.String(64), nullable=False) #path to js file where exectured


    def __repr__(self):
        return f'<Glitch id: {glitch_id} name: {name} javascript: {js_file}>'



class ImageChoice(db.Model):

    __tablename__ = "images"

    image_id    = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    url         = db.Column(db.String(128), nullable=False) #maybe bigger later?

    def __repr__(self):

        return f'<Image id: {self.image_id} url: {self.url}>'




def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    from server import app

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///images'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()