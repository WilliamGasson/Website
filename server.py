"""
server.py

"""

__date__ = "2023-03-09"
__author__ = "WilliamGasson"
__version__ = "0.1"


# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------



from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory
import os
from Chess import GameState
from Chess import Move
from Sudoku import GameState
from Sudoku import main

from Computer_Vision.src import predict, model_class, torch_helper


from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
import base64
import io
import datetime as dt
import logging


app = Flask(__name__)


@app.route("/hello_world")
def hello_world():
    return "hello_world"

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lensless")
def lensless():
    return render_template("lensless.html")

@app.route("/chess", methods=['GET', 'POST'])
def chess():
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']

        print(tag)
    wR1 = "a1"
    return render_template("chess.html", wR1=wR1)

@app.route("/articles")
def articles():
    return render_template("articles.html")


@app.route("/template")
def template():
    return render_template("template.html")

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']

        print(tag)
        return 'The credentials for %s' % (tag) 

    else:   
        return  render_template("test.html")



## image upload

UPLOAD_FOLDER = "tmp"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getByteSize(num, suffix='B') -> str:
    """
    Converts file size into byte size
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def getTimeStampString(tSec: float) -> str:
    """
    Saves time the file was saved
    """
    timstamp = dt.datetime.fromtimestamp(tSec)
    timstampStr = dt.datetime.strftime(timstamp, '%Y-%m-%d %H:%M:%S')
    return timstampStr

def getIconClassForFilename(fName):
    """
    Gets the icon for the particular file type
    """
    FILE_TYPES = [ "bmp", "cs", "css", "csv", "doc", "docx", "exe", "gif", "heic", "html", "java", "jpg", "js", "json", "jsx", "key", "m4p", "md", "mdx", "mov", "mp3", "mp4", "pdf", "php", "png", "pptx", "psd", "py", "raw", "rb", "sass", "scss", "sh", "sql", "svg", "tiff", "tsx", "ttf", "txt",  "xlsx", "xml", "yml"]
    fileExt = Path(fName).suffix
    fileExt = fileExt[1:] if fileExt.startswith(".") else fileExt
    fileIconClass = f"bi bi-filetype-{fileExt}" if fileExt in FILE_TYPES else "bi bi-file-earmark"
    return fileIconClass

# Show directory contents
def fObjFromScan(x):
    fileStat = x.stat()
    # return file information for rendering
    return {'name': x.name,
            'fIcon': "bi bi-folder-fill" if os.path.isdir(x.path) else getIconClassForFilename(x.name),
            'relPath': os.path.relpath(x.path, UPLOAD_FOLDER).replace("\\", "/"),
            'mTime': getTimeStampString(fileStat.st_mtime),
            'size': getByteSize(fileStat.st_size)}




# route handler
@app.route('/directory/', defaults={'reqPath': ''}, methods=['GET', 'POST'])
@app.route('/directory/<path:reqPath>')
def getFiles(reqPath):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('getFiles', reqPath=filename))
    
    
    # Join the base and the requested path
    # could have done os.path.join, but safe_join ensures that files are not fetched from parent folders of the base folder
    absPath = os.path.join(UPLOAD_FOLDER, reqPath)

    # Return 404 if path doesn't exist
    if not os.path.exists(absPath):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(absPath):
        return send_file(absPath)

    fileObjs = [fObjFromScan(x) for x in os.scandir(absPath)]
    # get parent directory url
    parentFolderPath = os.path.relpath(
        Path(absPath).parents[0], UPLOAD_FOLDER).replace("\\", "/")
    return render_template('directory.html', data={'files': fileObjs, 'parentFolder': parentFolderPath})




@app.route('/cv/', defaults={'reqPath': ''})
@app.route('/cv/<path:reqPath>')
def identifyImg(reqPath):
    # Join the base and the requested path
    # could have done os.path.join, but safe_join ensures that files are not fetched from parent folders of the base folder
    absPath = os.path.join(UPLOAD_FOLDER, reqPath)
    # get parent directory url

    FolderPath = os.path.relpath(Path(absPath).parents[0], UPLOAD_FOLDER).replace("\\", "/")
    
    # Return 404 if path doesn't exist
    if not os.path.exists(absPath):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(absPath):
        
        fileObjs = [fObjFromScan(x) for x in os.scandir(FolderPath)]
        print(absPath)
        img_path = absPath
        model_path = "../Computer_Vision/models/cifar10-resnet9.pth"
        # model_type = ResNet9(3, 10)

        pred_model = predict.predict(model_path)#, model_type)
        prediction = pred_model.predict_img(img_path)
        print('Predicted:', prediction)
        
        im = Image.open(img_path)
        newsize = (300, 300)
        im = im.resize(newsize)
        data = io.BytesIO()
        im.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        
        return render_template("cv.html", pred = prediction, img_data=encoded_img_data.decode('utf-8'))
    
        # return render_template('vision.html', data={'files': fileObjs, 'folder': FolderPath})
    
    return render_template('vision.html')




@app.route('/sudoku', methods=['GET', 'POST'])
def image_recognition():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('getFiles', reqPath=filename))
    
    return render_template("sudoku.html")





if __name__ == '__main__':
       app.run(port = 5000, debug = True)