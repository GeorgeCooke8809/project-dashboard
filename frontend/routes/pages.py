from flask import Blueprint, redirect, render_template, session
from projects import utils
import logging

pages = Blueprint("pages", __name__)


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
                           details = details,
                           )

@pages.route("/login", methods = ["GET"])
def login():
    if "admin" not in session:
        return render_template("login.html")
    
    return redirect("/admin-dashboard")
    

# ==================== Admin Pages ====================

@pages.route("/admin-dashboard", methods = ["GET"])
def admin_dashboard(): # ? Make admin dashboard include buttons to work on a project today?
    if "admin" not in session or session["admin"] != True:
        return redirect("/login")
    
    return render_template("admin-dashboard.html",
                           active_projects = utils.get_active_projects_overview()
                           )

@pages.route("/add-project", methods = ["GET"])
def add_project_page():
    if "admin" not in session:
        return redirect("/login")

    return render_template("add-project.html")

@pages.route("/inactive-projects", methods = ["GET"])
def inactive_projects_page(): # TODO: Add delete project
    if "admin" not in session:
        return redirect("/login")

    return render_template("inactive-projects.html",
                           inactive_projects = utils.get_inactive_projects()
                           )

@pages.route("/edit-project/<id>", methods = ["GET"])
def edit_project_page(id: int):
    if "admin" not in session:
        return redirect("/login")
    
    project_details = utils.get_project_details(id)
    if project_details["updated"] != None:
        updated_date = project_details["updated"].strftime("%Y-%m-%d")
    else:
        updated_date = None

    logging.info(f"{project_details = }")

    return render_template("edit-project.html",
                           details = project_details,
                           created = project_details["created"].strftime("%Y-%m-%d"),
                           updated = updated_date
                           )

@pages.route("/logout", methods = ["GET"])
def logout():
    if "admin" in session:
        session.pop("admin", None)

    return redirect("/login")