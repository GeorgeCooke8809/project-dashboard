from flask import Blueprint, redirect, render_template
from projects import utils

pages = Blueprint("pages", __name__)


# ==================== Main Pages ====================


@pages.route("/", methods = ["GET"])
def index():
    return render_template("index.html",
                           projects = [{
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }, 
                            {
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }, 
                            {
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }, 
                            {
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }, 
                            {
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }, 
                            {
                                "id": 1,
                                "name": "name",
                                "url": "google.com"
                            }]
                           )


# ==================== Admin Pages ====================