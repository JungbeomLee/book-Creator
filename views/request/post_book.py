from flask import Blueprint, request, jsonify
from views.function_file import _log_write, _mongoDB, _key_loader

import os

bp = Blueprint('flask_story_post', __name__, url_prefix='/post')

@bp.route('/story', methods=['POST'])
def post_story():
    try:
        # 쿠키 값 가져오기
        unique_key = request.form.get('unique_key')
        
        if not unique_key:
            _log_write.write_log(400, "No cookie provided")
            return jsonify({'load_book': False, 'error': 'No cookie provided'}), 400

        # DB에서 쿠키 값으로 데이터 가져오기
        MONGO_PASSWORD = _key_loader.mongodb_password()
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)
        db = client['cbook']
        queue = db['cbookCreatedPastInfo']
        query = {'key' : unique_key}

        results = queue.find_one(
            {'key': unique_key},
            sort=[('timestamp', -1)]  # timestamp 기준 오름차순 정렬 (가장 오래된 데이터)
        )
        story_data = results['past_story_kr']
        print(story_data)

        try : 
            story = story_data['content']
        except :
            story = story_data['contents']
        
        
        IMAGE_PATH = '/root/book-Creator/static/story_images/'
        files_in_directory = os.listdir(IMAGE_PATH)
        # 주어진 이름과 동일한 이름을 가진 이미지 파일 찾기
        matching_files = [file for file in files_in_directory 
                        if os.path.splitext(file)[0].split('_')[0] == unique_key]
        
        queue = db['cbookPCreateSucess']
        results = queue.delete_one(query)
        if story_data:
            _log_write.write_log(200, f"Successfully loaded story for cookie: {unique_key}")
            return jsonify({
                'load_book': True,
                'story': story,
                'title': story_data['title'],
                'options': story_data['options'],
                'image_path':f"{unique_key}_{len(matching_files)-1}.png"
            })

        
        else:
            _log_write.write_log(404, f"No story found for cookie: {unique_key}")
            return jsonify({'load_book': False, 'error': 'Story not found'}), 404
    
    except Exception as e:
        _log_write.write_log(500, f"An error occurred: {e}")
        return jsonify({'load_book': False, 'error': str(e)}), 500
