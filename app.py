from flask import Flask
from views.function_file import _key_loader, _log_write, _api_connection_test, _mongdoDB_test

import os

current_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_path)

def create_app() :
    app = Flask(__name__)

    from views.page import flask_main
    from views.page import flask_upload_info
    from views.page import flask_upload_image
    from views.page import flask_createBook
    from views.page import flask_book

    from views.request import post_info
    from views.request import post_image
    from views.request import post_createBook
    from views.request import post_bookCP
    from views.request import post_book
    from views.request import post_pastCreateBook

    app.register_blueprint(flask_main.bp)
    app.register_blueprint(flask_upload_info.bp)
    app.register_blueprint(flask_upload_image.bp)
    app.register_blueprint(flask_createBook.bp)
    app.register_blueprint(flask_book.bp)
    
    app.register_blueprint(post_info.bp)
    app.register_blueprint(post_image.bp)
    app.register_blueprint(post_createBook.bp)
    app.register_blueprint(post_bookCP.bp)
    app.register_blueprint(post_book.bp)
    app.register_blueprint(post_pastCreateBook.bp)

    return app

if __name__ == '__main__':
    # 키 로드 및 테스트
    API_KEY = _key_loader.api_key_load()
    PROJECT_ID = _key_loader.project_id_load()
    MONGO_PASSWORD = _key_loader.mongodb_password()

    api_status = _api_connection_test.api_connection_test(API_KEY, PROJECT_ID)
    mongdoDB_status = _mongdoDB_test.mongodb_connection_test(MONGO_PASSWORD)

    status = {'watsonx_api_key' : 500,
              'mongoDB' : 500}
    # 로그 작성
    # watsonx api connection test
    if api_status == 200:
        _log_write.write_log(200, "ServerStart(API connect): Connection successful.")
        status['watsonx_api_key'] = 200
    else:
        _log_write.write_log(api_status, f"ServerStart(API connect): Connection failed with status {api_status}")

    # mongdoDB connection test
    if mongdoDB_status == 200:
        _log_write.write_log(200, "ServerStart(DB connect): Connection successful.")
        status['mongoDB'] =200
    else:
        _log_write.write_log(api_status, f"ServerStart(DB connect): Connection failed with status {mongdoDB_status}")

    # watsonx && mongoDB status check
    if status['watsonx_api_key'] == 200 and status['mongoDB'] == 200 :
        app = create_app()
        app.run(port=5000,  host='0.0.0.0', debug=True)
