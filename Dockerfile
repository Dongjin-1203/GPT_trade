# Python 3.11 slim 이미지 기반
FROM python:3.11-slim

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 의존성 설치
COPY require.txt .
RUN apt-get update && \
    apt-get install -y fonts-nanum fontconfig && \
    fc-cache -fv && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r require.txt

# 전체 프로젝트 복사
COPY . .

# 실행 명령
CMD ["python", "run.py"]
