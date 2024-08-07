FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /code

# 종속성 파일 복사 및 설치
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# 애플리케이션 코드 복사
COPY ./ /code/

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

