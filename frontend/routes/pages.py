from flask import Blueprint, redirect, render_template, request, session, jsonify, url_for
from projects import utils
from configs import ADMIN_USERNAME, ADMIN_PASSWORD
import logging

pages = Blueprint("pages", __name__)

# TODO: Add admin add projects


# ==================== Main Pages ====================


@pages.route("/", methods = ["GET"])
def index():
    return render_template("index.html",
                           projects = utils.get_active_projects_overview()
                           )

@pages.route("/details/<id>", methods = ["GET"])
def details(id: int):
    try:
        details = utils.get_project_details(id)
    except ValueError:
        return render_template("404.html")

    return render_template("details.html",
                           details = details)

@pages.route("/login", methods = ["GET", "POST"])
def login(): # TODO: Split some off to api file
    if request.method == "POST":
        details = request.get_json()
        username = details["username"]
        password = details["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True
            session["admin"] = True

            return jsonify({
                "code": 200,
                "message": ""
            })
        else:
            return jsonify({
                "code": 401,
                "message": "Those login details are not valid."
            })
    else:
        if "admin" not in session:
            return render_template("login.html")
        
        return redirect("/admin-dashboard"
                        #admin = session["admin"] # TODO: Add logout in base based on admin flag here
                        )
    

# ==================== Admin Pages ====================

@pages.route("/admin-dashboard", methods = ["GET"])
def admin_dashboard():
    if "admin" not in session or session["admin"] != True:
        return redirect("/login")
    
    return render_template("admin-dashboard.html",
                           #admin = session["admin"],
                           active_projects = utils.get_active_projects_overview()
                           )

@pages.route("/add-project", methods = ["GET"])
def add_project_page():
    if "admin" not in session:
        return redirect("/login")

    return render_template("add-project.html")

@pages.route("/inactive-projects", methods = ["GET"])
def inactive_projects_page():
    if "admin" not in session:
        return redirect("/login")

    return render_template("inactive-projects.html",
                           #admin = session["admin"],
                           inactive_projects = utils.get_inactive_projects()
                           )

@pages.route("/edit-project/<id>", methods = ["GET"])
def edit_project_page(id: int):
    if "admin" not in session:
        return redirect("/login")
    
    project_details = utils.get_project_details(id)

    logging.info(f"{project_details = }")

    return render_template("edit-project.html",
                           details = project_details
                           )

@pages.route("/logout") # TODO: Move to api file
def logout():
    if "admin" in session:
        session.pop("admin", None)
    return redirect("/login")