from flask import Blueprint, render_template

bp = Blueprint('createbook', __name__, url_prefix='/')

# upload info page
@bp.route('/createbook')
def main_page() :
  return render_template('create_book.html')