from flask import Blueprint, render_template

bp = Blueprint('flask_upload_info', __name__, url_prefix='/upload')

# upload info page
@bp.route('/info')
def main_page() :
  return render_template('upload_info.html')