from flask import Flask, render_template, request,redirect,url_for, flash
import os
from Chess import GameState
from Chess import Move
#from Sudoku import GameState
#from Sudoku import main
from werkzeug.utils import secure_filename
from flask import send_from_directory



UPLOAD_FOLDER = "tmp"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/home")
def home():
    return render_template("home.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chess", methods=['GET', 'POST'])
def chess():
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']

        print(tag)
    wR1 = "a1"
    return render_template("chess.html", wR1=wR1)

@app.route("/img_rec")
def image_recognition():
    return render_template("img_rec.html")

@app.route("/upload_img", methods=["GET", "POST"])
def upload_image():
    return render_template("upload_img.html")

@app.route("/lensless")
def lensless():
    return render_template("lensless.html")

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

@app.route("/")
def hello_world():
    return "hello_world"




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
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template("upload.html")
    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
       app.run(port = 5000, debug = True)