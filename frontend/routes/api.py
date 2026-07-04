from configs import ADMIN_USERNAME, ADMIN_PASSWORD
from flask import Blueprint, jsonify, request, session
from projects import utils
import logging

api = Blueprint("api", __name__)

@api.route("/add-project", methods = ["POST"])
def add_project():
    details = request.get_json()

    if details["title"] == "":
        logging.info("Rejected add project - did not have title.")

        return jsonify({
            "code": 400,
            "message": "The name field it required."
        })
    
    try:
        utils.add_project(name = details["title"], url = details["url"], description = details["description"], updated = details["updated"], created = details["created"])
        logging.info("Project successfully added")
        return jsonify({
            "code": 200,
            "message": "Project added successfully."
        })
    except:
        logging.warning(f"Failed to add project. Error:")
        return jsonify({
            "code": 500,
            "message": "Something went wrong.",
        })
    
@api.route("/archive-project", methods = ["POST"])
def archive_project():
    details = request.get_json()

    try:
        utils.deactivate_project(details["id"])
        logging.info("Project successfully archived.")
        return jsonify({
            "code": 200,
            "message": ""
        })
    except ValueError:
        logging.warning(f"The project {details["id"] = } does not exist to archive")
        return jsonify({
            "code": 500,
            "message": "The project does not exist to archive."
        })
    except:
        logging.warning("Something unknown went wrong archiving the project.")
        return jsonify({
            "code": 500,
            "message": "Something went wrong archiving the project."
        })
    
@api.route("/restore-project", methods = ["POST"])
def restore_project():
    details = request.get_json()

    try:
        utils.activate_project(details["id"])
        logging.info("Project successfully restored")
        return jsonify({
            "code": 200,
            "message": ""
        })
    except ValueError:
        logging.warning(f"The project {details["id"] = } does not exist to restore")
        return jsonify({
            "code": 500,
            "message": "The project does not exist to restore."
        })
    except:
        logging.warning("Something unknown went wrong restoring the project.")
        return jsonify({
            "code": 500,
            "message": "Something went wrong restoring the project."
        })
    
@api.route("/edit-project", methods = ["POST"])
def edit_project():
    details = request.get_json()

    if details["title"] == "":
        logging.info("Rejected edit project - did not have title.")

        return jsonify({
            "code": 400,
            "message": "The name field it required."
        })
    
    try:
        utils.edit_project(project_id = details["id"], name = details["title"], url = details["url"], description = details["description"], created = details["created"], updated = details["updated"])
        logging.info("Project successfully edited")
        return jsonify({
            "code": 200,
            "message": "Project added successfully."
        })
    except:
        logging.warning(f"Failed to edit project. Error:")
        return jsonify({
            "code": 500,
            "message": "Something went wrong.",
        })

@api.route("/login", methods = ["POST"])
def login():
    details = request.get_json()

    if details["username"] == ADMIN_USERNAME and details["password"] == ADMIN_PASSWORD:
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