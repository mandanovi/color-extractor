from flask import Flask, render_template, after_this_request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os, glob
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'uploads')


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class UploadForm(FlaskForm):
    upload = FileField('Upload Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Wrong file. JPG, PNG only!')
    ])


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()
    return render_template("index.html", form=form)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    @after_this_request
    def delete(response):
        os.remove(image_path)
        return response

    form = UploadForm()
    if form.validate_on_submit():
        f = form.upload.data
        print(f)
        name = secure_filename(f.filename)
        full_filename = os.path.join('static/uploads/', name)
        f.save(full_filename)
        image_path = f"static/uploads/{f.filename}"
        user_img = Image.open(image_path)
        img_shape = np.array(user_img)
        clt = KMeans(n_clusters=10)
        clt.fit(img_shape.reshape(-1, 3))
        clt_clusters = clt.cluster_centers_
        print(clt_clusters)
        return render_template("upload.html", form=form, image=image_path, colors=clt_clusters)

    return render_template("upload.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)