from flask import Blueprint, request, jsonify

from views.function_file import _mongoDB, _key_loader

bp = Blueprint('post_bookCP', __name__, url_prefix='/post')

@bp.route('/bookcp', methods=['POST'])
def check_completion() :
    if request.method == 'POST':
        unique_key = request.form.get('unique_key')
        
        MONGO_PASSWORD = _key_loader.mongodb_password()
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)

        db = client['cbook']
        collection = db['cbookPCreateSucess']

        query = {'key' : unique_key}
        results = collection.find_one(query)

        if results == None :
            return jsonify({'status': 'pending'})
        else :
            return jsonify({'status': 'completed'})