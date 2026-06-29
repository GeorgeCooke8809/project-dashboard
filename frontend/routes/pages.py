from flask import Blueprint, redirect, render_template, request, session, jsonify, url_for
from projects import utils
from configs import ADMIN_USERNAME, ADMIN_PASSWORD

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

@pages.route("/details/<id>", methods = ["GET"])
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
        print(f"{session = }")
        if "admin" not in session:
            return render_template("login.html")
        
        return redirect("/admin-dashboard",
                        #admin = session["admin"] # TODO: Add logout in base based on admin flag here
                        )
    

# ==================== Admin Pages ====================

@pages.route("/admin-dashboard", methods = ["GET"])
def admin_dashboard():
    if "admin" not in session or session["admin"] != True:
        return redirect(url_for("pages.login"))
    
    return render_template("admin-dashboard.html",
                           #admin = session["admin"]
                           )

@pages.route("/logout")
def logout():
    if "admin" in session:
        session.pop("admin", None)
    return redirect("/login")