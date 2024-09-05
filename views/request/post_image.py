from flask import Blueprint, request, jsonify
from views.function_file import _log_write

import os

bp = Blueprint('flask_image_post', __name__, url_prefix='/post')

UPLOAD_FOLDER = 'upload_images/'

@bp.route('/image', methods=['POST'])
def uploaded_image():
    try:
        if request.method == 'POST':
            image = request.files.get('upload_image')
            unique_key = request.form.get('unique_key')
            
            filename = f'{unique_key}.png'
            saved_files = []

            # 업로드 폴더가 존재하지 않으면 생성
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            # 파일이 존재하면 삭제
            if os.path.exists(file_path):
                os.remove(file_path)
                _log_write.write_log(200, f"Existing file deleted: {file_path}")
            image.save(file_path)
            saved_files.append(file_path)
            
            if saved_files:
                _log_write.write_log(200, f"Successfully uploaded")
                return jsonify({'posting_image': True})
            else:
                _log_write.write_log(400, "No files were uploaded.")
                return jsonify({'posting_image': False})
            
    except Exception as e:
        _log_write.write_log(500, f"An error occurred while saving image")
        return jsonify({'posting_image': False})