from flask import Blueprint, render_template

bp = Blueprint('upload_image', __name__, url_prefix='/upload')

# upload info page
@bp.route('/image')
def main_page() :
  return render_template('upload_image.html')