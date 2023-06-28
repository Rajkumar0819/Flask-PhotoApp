from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Image
from . import db
import base64

# import mimetypes

views = Blueprint("views", __name__)


@views.route("/")
def index_page():
    return render_template("index.html")


@views.route("/images", methods=["GET", 'POST'])
@login_required
def images_page():
    if request.method == "POST":
        image = request.files["photo"]
        if not image:
            flash("No Image added", category="error")
        else:
            mimetype = image.mimetype
            img = Image(image_source=image.read(), user_id=current_user.id, mimetype=mimetype)
            db.session.add(img)
            db.session.commit()
            flash("Image uploaded successfully", category='success')
    user_images = Image.query.filter_by(user_id=current_user.id).all()
    for image in user_images:
        image.image_source = base64.b64encode(image.image_source).decode("utf-8")

    return render_template("images.html", user=current_user, user_images=user_images)


@views.route("/images/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    image = Image.query.filter_by(user_id=current_user.id, id=image_id).first()
    db.session.delete(image)
    db.session.commit()
    flash("Image deleted successfully", category="success")
    return redirect(url_for("views.images_page"))
