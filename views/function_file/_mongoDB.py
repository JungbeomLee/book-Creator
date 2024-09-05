import pymongo
from views.function_file import _log_write

def mongodb_connection(MONGO_PASSWORD):
    # MongoDB 연결 정보
    mongo_host = 'localhost'  # 또는 컨테이너의 IP 주소
    mongo_port = 27017
    mongo_user = 'user'
    mongo_password = MONGO_PASSWORD

    # MongoDB에 연결
    try:
        client = pymongo.MongoClient(f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}')

        return client
    except pymongo.errors.ConnectionFailure as e:
        _log_write.write_log(client, f"ServerStart(DB connect) : Connection failed: {e}")
        return 500
