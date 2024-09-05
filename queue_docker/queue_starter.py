from fuction_file import _mongoDB, _key_loader, _log_write

import queue_processing
import time

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

    db = client['cbook']
    queue = db['cbookCreateQueue']

    while True :
        task = queue.find_one()
        if task:
            _log_write.write_log(200, "Element found, start queue process...")
            star_first_queue()
            _log_write.write_log(200, "queue process done")
            if 'client' in locals():
                client.close()

        # 5초 대기
        time.sleep(5)
