from configs import ADMIN_PASSWORD
from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)