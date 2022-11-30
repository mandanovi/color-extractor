from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


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
        name = f.filename
        name = secure_filename(name)
        f.save(os.path.join("static/uploads/", name))
        image_path = f"static/uploads/{f.filename}"
        user_img = Image.open(image_path)
        img_shape = np.array(user_img)
        clt = KMeans(n_clusters=10)
        clt_fit = clt.fit(img_shape.reshape(-1,3))
        clt_label = clt.labels_
        clt_clusters = clt.cluster_centers_
        print(clt_clusters)
        return render_template("upload.html", form=form, image=image_path, colors=clt_clusters)
    return render_template("upload.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)