from flask import Blueprint, redirect, render_template
from projects import utils

pages = Blueprint("pages", __name__)

# TODO: Add admin add projects


# ==================== Main Pages ====================


@pages.route("/", methods = ["GET"])
def index():
    return render_template("index.html",
                           projects = [{
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }]
                           )

@pages.route("/details/<id>", methods = ["GEt"])
def details(id: int):
    try:
        details = utils.get_project_details(id)
    except ValueError:
        details = {
        "id": 1,
        "name": "Name",
        "url": "google.com",
        "description": "lorem ipsum",
        "created": "fjkhgkj",
        "created_readable": "07/05/09"
    }
        #return render_template("404.html")

    return render_template("details.html",
                           details = details)

# ==================== Admin Pages ====================