from flask import Blueprint, jsonify, render_template

gen_bp = Blueprint('gen', __name__)

@gen_bp.route("/", methods=['GET'])
def getUsers():

    return "Welcome to Just a Doodle's Social API!"
