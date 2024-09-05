from flask import Blueprint, render_template

bp = Blueprint('flask_book', __name__, url_prefix='/')

# upload info page
@bp.route('/book')
def main_page() :
  return render_template('book.html')