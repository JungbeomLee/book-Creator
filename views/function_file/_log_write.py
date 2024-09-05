import logging

def write_log(status, message):
    log = logging.getLogger("api_key_logger")

    if not log.handlers:
        # 로그 출력 형식 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 콘솔에 로그 출력
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)

        # 로그를 파일에 출력
        file_handler = logging.FileHandler('logs/log.log')
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    # 로그 수준 설정 및 메시지 기록
    if status == 200:
        log.setLevel(logging.INFO)
        log.info(message)
    else:
        log.setLevel(logging.ERROR)
        log.error(message)