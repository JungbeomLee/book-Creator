from views.function_file import _mongoDB, _log_write

import pymongo

def mongodb_connection_test(MONGO_PASSWORD):
    # MongoDB에 연결
    try:
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)

        if client == 500 :
            return 500

        db = client.admin  # 연결 테스트를 위해 admin 데이터베이스 사용
        db.command('ping')

        return 200
    except pymongo.errors.ConnectionFailure as e:
        _log_write.write_log(client, f"ServerStart(DB connect) : Connection ping failed: {e}")
        return 500
    finally:
        if 'client' in locals():
            client.close()