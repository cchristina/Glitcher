"""Glitch Art."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

from datetime import datetime, timedelta 

from model import ImageChoice, Glitch, connect_to_db, db




# from glitchstuff import *

from datetime import * 




import glitchstuff as gs

from PIL import Image








app = Flask(__name__)



# Required to use Flask sessions and the debug toolbar
# app.secret_key = "a1b2c3"
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


dropzone = Dropzone(app)
# Dropzone settings
#https://medium.com/@dustindavignon/upload-multiple-images-with-python-flask-and-flask-dropzone-d5b821829b1d
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'



# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/images/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



# @app.route('/')
# def index():
#     """Homepage."""
#     return render_template("home.html")



###START WORKING COODE ###
# @app.route('/', methods=['GET', 'POST'])
# def index():
    
#     # set session for image results
#     if "file_urls" not in session:
#         session['file_urls'] = []
#     # list to hold our uploaded image urls
#     file_urls = session['file_urls']
#     # handle image upload from Dropzone
#     if request.method == 'POST':
#         file_obj = request.files
#         for f in file_obj:
#             file = request.files.get(f)
            
#             # save the file with to our photos folder
#             filename = photos.save(
#                 file,
#                 name=file.filename    
#             )
#             # append image urls
#             file_urls.append(photos.url(filename))
            
#         session['file_urls'] = file_urls
#         return "uploading..."
#     # return dropzone template on GET request    
#     return render_template('index.html')
# @app.route('/results')
# def results():
    
#     # redirect to home if no images to display
#     if "file_urls" not in session or session['file_urls'] == []:
#         return redirect(url_for('index'))
        
#     # set the file_urls and remove the session variable
#     file_urls = session['file_urls']
#     session.pop('file_urls', None)

#     for fu in file_urls:
#         #../static/images/
#         splt_fu = fu.split('/')
#         new_url = "/static/images/uploads/" + splt_fu[-1]
#         new_image = ImageChoice(url=new_url)

#         db.session.add(new_image)
#         print(new_image)
#         db.session.commit()

    
#     return render_template('results.html', file_urls=file_urls)
### END WORKING CODE ###



### START NOT WORKING ###
@app.route('/')
def index():
    """Homepage."""
    return render_template("home.html")




@app.route('/uploadImage', methods=['GET', 'POST'])
def upload_image():
    
    # set session for image results
    if "file_urls" not in session:

        session['file_urls'] = []


    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':

        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))

            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request  

    return render_template('uploadimage.html')



@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('upload_image'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)

    for fu in file_urls:
        #../static/images/

        splt_fu = fu.split('/')
        new_url = "../static/images/uploads/" + splt_fu[-1]
        new_image = ImageChoice(url=new_url)

        db.session.add(new_image)
        print(new_image)
        db.session.commit()

    
    return render_template('results.html', file_urls=file_urls)

###END NOT WORKINH ###

@app.route('/mainpage', methods = ["GET", "POST"])
def mainpage():


    images = ImageChoice.query.all()

    ##start maybe###
    if "file_urls" not in session:
        session['file_urls'] = []


    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    ###end maybr ###

    if (request.method=="GET"):
        return render_template("mainpage.html", images=images) #rename this eventuallly 
    
    else:

        ###START MAYBE ###
        # if session['file_urls']:
        #     file_obj = request.files
        #     for f in file_obj:
        #         file = request.files.get(f)
                
        #         # save the file with to our photos folder
        #         filename = photos.save(
        #             file,
        #             name=file.filename    
        #         )
        #         # append image urls
        #         file_urls.append(photos.url(filename))
        #     file_urls = session['file_urls']
        #     session.pop('file_urls', None)

        # for fu in file_urls:
        #     #../static/images/

        #     splt_fu = fu.split('/')
        #     new_url = "../static/images/uploads/" + splt_fu[-1]
        #     new_image = ImageChoice(url=new_url)

        #     db.session.add(new_image)
        #     print(new_image)
        #     db.session.commit()

                
        #     session['file_urls'] = file_urls
        #  session['file_urls'] = []
        # return redirect('/')
        ### END MAYBE ###   

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




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageUpload', methods=['GET', 'POST'])
def upload_file():

    print(request.form.get('dropzoneUpload'), request.files, "*************&&&&&&&&&&&&&&&&&&")
    new_image = Image.open(request.form.get('dropzoneUpload'))
    new_image.save('UPLOAD_FOLDER'+filename)




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