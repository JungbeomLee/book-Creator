from flask import Blueprint, render_template

bp = Blueprint('flask_main', __name__, url_prefix='/')

# main page
@bp.route('/')
def main_page() :
  return render_template('index.html')