from flask import Flask, render_template, request,redirect,url_for
import os
from Chess import GameState
from Chess import Move



app = Flask(__name__)

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

if __name__ == '__main__':
       app.run(port = 5000, debug = True)