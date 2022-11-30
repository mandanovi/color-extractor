from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from colorthief import ColorThief


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = "static/uploads"


class UploadForm(FlaskForm):
    upload = FileField('Upload Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()
    return render_template("index.html", form=form)


@app.route("/upload", methods=["GET","POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.upload.data
        name = secure_filename(f.filename)
        f.save(os.path.join("static/uploads/", name))
        image_path = f"static/uploads/{f.filename}"
        print(image_path)
        color_thief = ColorThief(image_path)
        top_colors = color_thief.get_palette(color_count=11)
        return render_template("upload.html", form=form, image=image_path, colors=top_colors)
    return render_template("upload.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)