from flask import Blueprint, request, jsonify
from views.function_file import _log_write, _mongoDB, _key_loader

import uuid

bp = Blueprint('flask_upload_info_post', __name__, url_prefix='/post')

@bp.route('/info', methods=['POST'])
def uploaded_info():
    try:
        # 폼 데이터 수신
        child_name = request.form['name']
        child_age = request.form['age']
        child_sex = request.form['sex']
        child_thema = request.form['thema']
        child_favorite = request.form['favorite']
        child_teach = request.form['teach']

        # 데이터 딕셔너리 구성
        unique_key = str(uuid.uuid4())
        data = {
            'key' : unique_key,
            'name': child_name,
            'age': child_age,
            'sex': child_sex,
            'thema': child_thema,
            'favorite': child_favorite,
            'teach': child_teach
        }

        MONGDO_PASSWORD = _key_loader.mongodb_password()
        client = _mongoDB.mongodb_connection(MONGDO_PASSWORD)

        db = client['cbook']
        collection = db['cbookCreateInfo']
        collection.insert_one(data)

        if 'client' in locals():
            client.close()

        # 로그 기록: 성공적인 파일 저장
        _log_write.write_log(200, f"cBookInfoInsert(info insert) : Successfully saved {child_name}")

        # 성공적인 응답 반환
        return jsonify({'posting_name': True, 'unique_key' : unique_key})
    
    except Exception as e:
        # 예외 발생 시 로그 기록
        _log_write.write_log(500, f"cBookInfoInsert(info insert) : Error occurred while saving {child_name}: {str(e)}")
        
        # 오류 응답 반환
        return jsonify({'posting_name': False})