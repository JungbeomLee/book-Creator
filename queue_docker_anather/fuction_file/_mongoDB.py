from fuction_file import _log_write

import pymongo

def mongodb_connection(MONGO_PASSWORD):
    # MongoDB 연결 정보
    mongo_host = '172.17.0.2'  # 또는 컨테이너의 IP 주소
    mongo_port = 27017
    mongo_user = 'user'
    mongo_password = MONGO_PASSWORD

    # MongoDB에 연결
    try:
        client = pymongo.MongoClient(f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}')
        _log_write.write_log(200, 'MongoDB connection successful.')
        return client
    except pymongo.errors.ConnectionFailure as e:
        _log_write.write_log(500, f'ConnectionFailure: {e}')
        return None
    except pymongo.errors.ConfigurationError as e:
        _log_write.write_log(500, f'ConfigurationError: {e}')
        return None
    except pymongo.errors.OperationFailure as e:
        _log_write.write_log(500, f'OperationFailure: {e}')
        return None
    except pymongo.errors.PyMongoError as e:
        _log_write.write_log(500, f'PyMongoError: {e}')
        return None
