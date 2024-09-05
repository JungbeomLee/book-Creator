from flask import Blueprint, request, jsonify
from views.function_file import _log_write, _mongoDB, _key_loader

import datetime

bp = Blueprint('flask_book_get', __name__, url_prefix='/post')

@bp.route('/makebook', methods=['POST'])
def get_makebook():
    try:
        if request.method == 'POST':
            unique_key = request.form.get('unique_key')
            time = datetime.datetime.now()

            MONGDO_PASSWORD = _key_loader.mongodb_password()
            client = _mongoDB.mongodb_connection(MONGDO_PASSWORD)

            db = client['cbook']
            queue = db['cbookCreateQueue']
            collection = db['cbookCreateInfo']

            query = {'key' : unique_key}
            results = collection.find_one(query)

            document = {
                'key': unique_key,
                'timestamp': time,
                'name': results['name'],
                'age': results['age'],
                'sex': results['sex'],
                'thema': results['thema'],
                'favorite': results['favorite'],
                'teach': results['teach']
            }
            queue.insert_one(document)
            
            _log_write.write_log(200, f"Enqueued: {time}")

            if 'client' in locals():
                client.close()

            return jsonify({'create_book': 200})
    except Exception as e:
        error_message = f"Error in get_makebook: {str(e)}"
        _log_write.write_log(500, error_message)
        return jsonify({'error': 'An error occurred', 'details': error_message}), 500
