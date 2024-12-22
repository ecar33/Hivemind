from flask import Blueprint, render_template

hive_bp = Blueprint('hive', __name__, url_prefix='/hive')

@hive_bp.route('/')
def index():
    return "Hive #1"