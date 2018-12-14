
from sqlalchemy import func
from model import Glitch
from model import ImageChoice

from model import connect_to_db, db
from server import app


def load_images():
    """Load images into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    ImageChoice.query.delete()

    # Read u.user file and insert data
    for row in open("static/seed_data/images2"):
        row = row.rstrip()
        image_id , image_path = row.split("|")
        image = ImageChoice(image_id=image_id, url=image_path)
        # We need to add to the session or it won't ever be stored
        db.session.add(image)
        print(image)

    # Once we're done, we should commit our work
    db.session.commit()






if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_images()

