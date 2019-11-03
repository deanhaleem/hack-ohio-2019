#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import json
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
from PIL import Image #pip install Pillow
from io import BytesIO
from similarity import *
from similaritySift import *
import glob

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
dataFile = 'data.txt'
app = Flask(__name__)
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
def getMatches(best_scores, best_images, center):
    for i,best_i in enumerate(best_scores):
            diff1 = abs(best_scores[i]-center) 
            for j,best_j in enumerate(best_scores):
                diff2 = abs(best_scores[j]-center)
                if diff2 < diff1:
                    best_scores[i], best_scores[j] = best_scores[j], best_scores[i]
                    best_images[i], best_images[j] = best_images[j], best_images[i]
    return best_images
                    


def getData(path):
    f = open(path, "r")
    lines = []
    imageData = {}

    for i, line in enumerate(f):
        formatted = json.loads(line)

        waterImages = formatted['water']
        natureImages = formatted['nature']
        buildingImages = formatted['buildings']
        

        
    return waterImages, natureImages, buildingImages

def analyze_image(url):
    os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = "ceb12c15a400458eb6884a6dc119986b"
    os.environ['COMPUTER_VISION_ENDPOINT'] = "https://deanhaleem.cognitiveservices.azure.com/"

    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    analyze_url = endpoint + "vision/v2.1/analyze"

    
    # Set image_path to the local path of an image that you want to analyze.
    image_path = url

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    return analysis

@app.route('/', methods=['GET', 'POST'])
def home():
    scores = []
    imagesToRank = []
    waterImages, natureImages, buildingImages = getData('data.txt')
    if request.method == 'POST':
        label = request.form['projectFilepath']
        print(label) 
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('index.html')   
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('index.html')
        if file:
            uploaded_files = request.files.getlist("file")
            # print(uploaded_files)
            array = []
            picArr = []
            for f in uploaded_files:
                name = extractName(f.filename)
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
                # print(file_path)
                f.save(file_path)
                picArr.append(file_path)
                extractedData = analyze_image(file_path) 
                # tags = extractedData['descriptions']['tags']
                # mylist = [f for f in glob.glob("redditImages/*.jpg")]
                if label == 'water':
                    histScore = similarityScore(file_path, waterImages)
                    siftScore = SiftsimilarityScore(file_path, waterImages)
        
                
                if label == 'nature':
                    histScore = similarityScore(file_path, natureImages)
                    siftScore = SiftsimilarityScore(file_path, natureImages)


                if label == 'building' or label == 'buildings':
                    histScore = similarityScore(file_path, buildingImages)
                    siftScore = SiftsimilarityScore(file_path, buildingImages)
          
                finalScore = histScore[0]*0.6 + siftScore[0]*0.4
                print(finalScore)

                if finalScore < 0.7 and finalScore > 0.1:
                    
                    print('Nice Pic')
                    scores.append(finalScore)
                    imagesToRank.append(file_path)
                else:
                    print('time to hang up your camera')

            
                    
                

                array.append(extractedData)
            rankedImgs = getMatches(scores, imagesToRank, 0.4)
            print(rankedImgs[0])

            
           


            
        return render_template('pages/display.html', title='Upload', pics=rankedImgs)
    else:
        return render_template('pages/placeholder.home.html', please=4, p=4)

def extractName(name):
    return os.path.basename(name)

# @app.route('/')
# def home():
#     arr = ["static/img/Items-Extras.png"]
#     return render_template('pages/placeholder.home.html', please=4, p=4, pics=arr)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/printf')
def printf():
    return '<p>Hello</p>'

@app.route('/gallery')
def gallery():
    return render_template('pages/gallery.html')

@app.route('/improvement')
def improvement():
    return render_template('pages/improvement.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
