"""Glitch Art."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime, timedelta 

from model import ImageChoice, Glitch, connect_to_db, db

# from glitchstuff import *

from datetime import * 


import glitchstuff as gs

from PIL import Image

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "a1b2c3"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("home.html")

@app.route('/mainpage', methods = ["GET", "POST"])
def mainpage():

    images = ImageChoice.query.all()
    

    if (request.method=="GET"):
        return render_template("mainpage.html", images=images) #rename this eventuallly 
    
    else:

        newimages = request.form.getlist('imagelist')
        glitchtype = request.form.get('glitchtype')




        # image1 = Image.open(request.form.get("imagelist")[3:])
        # image2 = Image.open(request.form.get("imagelist2")[3:])

        image1 = Image.open(newimages[0][3:])




        if (len(newimages) ==2):
            image2 = Image.open(newimages[1][3:])
        else:
            image2 = Image.open(newimages[0][3:])


        image1 = image1.resize((min(800, int(image1.size[0]*800/image1.size[1])),
                min(800, int(image1.size[1]*800/image1.size[0]))))

        image2 = image2.resize(
            (min(800, int(image2.size[0]*800/image2.size[1])),
                min(800, int(image2.size[1]*800/image2.size[0]))))





        img3String = ("./static/images/generated/"+str(datetime.now())[-6:]+".gif") 


        if (glitchtype == "pixely"):
           image3 = gs.pixelate_two_alt(image1, image2, 8, img3String) 
        
        elif(glitchtype=="grid"):
            image3 = gs.doub_grid(image2, 32, img3String)
    
        image3 = image3.resize(
            (min(800, int(image3.size[0]*800/image3.size[1])),
                min(800, int(image3.size[1]*800/image3.size[0]))))
        # image3.resize((800,800))


        image3.save(img3String)

        canvas_width = image1.size[0]
        canvas_height = image1.size[1]







        #str(datetime.now())+".jpg"



        return render_template("glitchpage.html", images = images, oldImage = (request.form.get("imagelist")[3:]), newImage=img3String, canvas_height = canvas_height, canvas_width = canvas_width)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug


    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')