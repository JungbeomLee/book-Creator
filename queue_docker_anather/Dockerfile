# Step 1: Python 3.10 베이스 이미지 사용
FROM python:3.10.11

# Step 2: 작업 디렉토리 설정
WORKDIR /app

# Step 3: 필요한 파일들 복사
COPY . /app

# Step 4: 의존성 설치
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: 환경 변수 설정 (필요할 경우)
# ENV 환경변수_이름 환경변수_값

# Step 6: 컨테이너 실행 시 실행할 명령어 설정
ENTRYPOINT python queue_starter.py
