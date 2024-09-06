from fuction_file import _mongoDB, _key_loader, _log_write

import queue_processing
import time
import os

current_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_path)

def star_first_queue() :
    queue = queue_processing.QUEUE_PROCESSING()
    queue.get_older_request()

def mongo_client(MONGO_PASSWORD) :
    client = _mongoDB.mongodb_connection(MONGO_PASSWORD)
    return client

if __name__ == "__main__" :
    _log_write.write_log(200, "Queue starter started")
    MONGO_PASSWORD = _key_loader.mongodb_password()
    client = mongo_client(MONGO_PASSWORD)

    client.server_info()  # 연결 확인

    db = client['cbook']
    queue = db['cbookPastCreateQueue']

    while True :
        task = queue.find_one()
        if task:
            _log_write.write_log(200, "Element found, start queue process...")
            star_first_queue()
            _log_write.write_log(200, "queue process done")

        # 5초 대기
        time.sleep(5)
