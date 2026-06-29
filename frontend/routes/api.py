from configs import ADMIN_PASSWORD
from flask import Blueprint, jsonify, request
from projects import utils
import logging

api = Blueprint("api", __name__)

@api.route("/add-project", methods = ["POST"])
def add_project():
    details = request.get_json()
    
    try:
        utils.add_project(name = details["title"], url = details["url"], description = details["description"])
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
            "error": ""
        })