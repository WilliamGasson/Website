from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory
import os
# from Chess.src import GameState
# from Chess.src import Move
#from Sudoku import GameState
#from Sudoku import main
from werkzeug.utils import secure_filename
from pathlib import Path
import datetime as dt

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "hello_world"

@app.route("/home")
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

@app.route("/temp")
def temp():
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
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
FILE_TYPES = [ "bmp", "cs", "css", "csv", "doc", "docx", "exe", "gif", "heic", "html", "java", "jpg", "js", "json", "jsx", "key", "m4p", "md", "mdx", "mov", "mp3", "mp4", "pdf", "php", "png", "pptx", "psd", "py", "raw", "rb", "sass", "scss", "sh", "sql", "svg", "tiff", "tsx", "ttf", "txt",  "xlsx", "xml", "yml"]
UPLOAD_FOLDER = "tmp"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/img_rec', methods=['GET', 'POST'])
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
    return render_template("img_rec.html")

@app.route("/upload_img", methods=["GET", "POST"])
def upload_image():
    return render_template("upload_img.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
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
            return redirect(url_for('getFiles', reqPath=filename)) # 'getFiles' name of function to look for
    return render_template("upload.html")


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def getReadableByteSize(num, suffix='B') -> str:
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
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d %H:%M:%S')
    return tStr

def getIconClassForFilename(fName):
    """
    Gets the icon for the particular file type
    """
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
            'size': getReadableByteSize(fileStat.st_size)}

# route handler
@app.route('/directory/', defaults={'reqPath': ''})
@app.route('/directory/<path:reqPath>')
def getFiles(reqPath):
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


if __name__ == '__main__':
       app.run(port = 5000, debug = True)