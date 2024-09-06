from fuction_file import _key_loader, _mongoDB, _log_write
from create_book import face_analyze, create_bookstory, create_image_prom, create_image
import datetime
import time

class QUEUE_PROCESSING:
    def __init__(self):
        self.API_KEY = _key_loader.api_key_load()
        self.OPENAI_KEY = _key_loader.openai_api_key_load()
        self.STABILITY_KEY = _key_loader.stability_key()
        self.PROJECT_ID = _key_loader.project_id_load()
        self.MONGO_PASSWORD = _key_loader.mongodb_password()

    def mongo_client(self, MONGO_PASSWORD):
        client = _mongoDB.mongodb_connection(MONGO_PASSWORD)
        return client

    def task_process(self, task, retry_count=3):
        try:
            # create story
            cbook = create_bookstory.CREATE_STORY(self.API_KEY, self.OPENAI_KEY, self.PROJECT_ID, self.MONGO_PASSWORD, task)
            en_story, kr_story = cbook.create_book()

            # analyzing image
            facea_analyze = face_analyze.FACE_ANALYZE(task, self.OPENAI_KEY)
            analyzed_image = facea_analyze.create_analyzed_improm()

            unique_key = task['key']
            timestamp = datetime.datetime.now()
            name = task['name']
            age = task['age']
            sex = task['sex']
            theme = task['thema']
            favorite = task['favorite']
            teach = task['teach']
            past_stroy_en = en_story
            past_story_kr = kr_story
            face_info = analyzed_image

            client = self.mongo_client(self.MONGO_PASSWORD)
            db = client['cbook']
            queue = db['cbookCreatedPastInfo']
            document = {
                'key': unique_key,
                'timestamp': timestamp,
                'name': name,
                'age': age,
                'sex': sex,
                'thema': theme,
                'favorite': favorite,
                'teach': teach,
                'past_stroy_en': past_stroy_en,
                'past_story_kr': past_story_kr,
                'face_info': face_info
            }
            queue.insert_one(document)

            # create image prom
            query = {'key': unique_key}
            results = queue.find_one(query)
            image_prompter = create_image_prom.IMAGE_PROM(self.API_KEY, self.OPENAI_KEY, self.PROJECT_ID, self.MONGO_PASSWORD, unique_key)
            image_prom = image_prompter.create_prom(results)

            # create image
            create_image.create_image(self.STABILITY_KEY, unique_key, image_prom)

            # key data delete
            queue = db['cbookCreateQueue']
            queue.delete_one({"key": unique_key})

            # add to success queue
            queue = db['cbookPCreateSucess']
            document = {
                'key': unique_key,
            }
            queue.insert_one(document)

        except Exception as e:
            _log_write.write_log(500, f"오류 발생: {str(e)}")
            if retry_count > 0:
                _log_write.write_log(500, f"재시도 {retry_count}회 남음. 5초 후 다시 시도합니다.")
                time.sleep(5)  # 5초 대기 후 재시도
                self.task_process(task, retry_count - 1)
            else:
                _log_write.write_log(500, "재시도 횟수 초과. 작업을 중단합니다.")

        finally:
            if 'client' in locals():
                client.close()

    def get_older_request(self):
        client = self.mongo_client(self.MONGO_PASSWORD)
        db = client['cbook']
        queue = db['cbookCreateQueue']

        task = queue.find_one(sort=[('timestamp', 1)])
        if task:
            _log_write.write_log(200, f"Start Processing task: {task['timestamp']}")
            self.task_process(task)

        if 'client' in locals():
            client.close()
