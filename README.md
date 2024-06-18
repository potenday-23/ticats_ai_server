# 티켓 사진 OCR 서버

티켓 사진의 텍스트로 추출하는 FastAPI 기반 프로젝트<br>
✔ 배포 웹사이트 : 배포 이전 상태 <br>
✔ Tech : FastAPI, SQLAlchemy, pydantic, postgresql, JWT, Alembic, Docker, AWS<br>

## Convention
- Camel Case(클래스)와 Snake Case(함수명) 구분
- 중복된 파라미터 최소화
- 함수에 대한 정의는 """로 시작
- 타입 힌트
- 주석은 최소화 + 코드 위에 간결하게 작성
- 비슷한 함수는 클래스로 묶기
- 미래에 쓸 것 같은 코드는 과감히 제외 (정말 쓸거라면 # TODO 주석으로)

## Summary

- 사진의 텍스트를 추출하는 AI 서버

## Skils

언어 및
프레임워크: ![Static Badge](https://img.shields.io/badge/Python-3.10-Blue) ![Static Badge](https://img.shields.io/badge/FastAPI-0.104.1-Blue)<br/>
데이터베이스 및
테스트: ![Static Badge](https://img.shields.io/badge/PostgreSQL-13-Green) ![Static Badge](https://img.shields.io/badge/Pytest-7.4.3-Pink) <br/>
배포 : ![Static Badge](https://img.shields.io/badge/Linux-Red) ![Static Badge](https://img.shields.io/badge/AWS-Orange)![Static Badge](https://img.shields.io/badge/Docker-Blue) <br/>

## Installation

1. 환경변수 설정
   ```env
   SECRET_KEY=e068f0399d3729db42eafdc56ca258ff3954c38a24ac423a6d5b15005378785c
   ```
2. 라이브러리 설치(python 3.9버전)
   ```bash
      pip install requirements.txt
   ```
3. 엘리스 미니 프로젝트 실행
    ```bash
   alembic upgrade head
   uvicorn main:app --reload
    ```
   - http://127.0.0.1:8000/docs

## 디렉터리 구조

- 3-Tier Architecture 방식 적용
- 관련 TIL : [[ocr #3] 디렉터리 구조화](https://www.notion.so/gabang2/elice-3-c9a18a905bd84e0dabcfbd4b7806db3e)

```angular2html
├─app
│  ├─config
│  ├─models
│  ├─routers
│  ├─schemas
│  ├─services
├─migrations
│  ├─versions
├─tests
│  └─routers
```

## Git Convention

- github-flow를 따름
- branch Convention
  ```angular2html
    issuename_#10
  ```
- commit Convention
  ```
  Feat #10 : 특정 기능 추가
  ```

## Running Tests

Test
=> tests 폴더 Run
> ![image](https://github.com/gabang2/elice_mini_project/assets/82714785/eeb3c59c-a25c-4437-9a0e-4c8571598bdc)
![Static Badge](https://img.shields.io/badge/Test_Passed-4/5-green)<br/>

## API 문서

![image](https://github.com/gabang2/elice_mini_project/assets/82714785/4324a516-ee70-4be5-8858-1e9f5c353689)
[API 문서 바로가기👈](http://54.180.102.238:8080/docs#/)

## Architecture

![image](https://github.com/gabang2/elice_mini_project/assets/82714785/9011fff4-2492-4e2e-a0a1-f7dc275d5fc5)

## TIL

### 전체 TIL 링크

- [Elice Mini Project](https://www.notion.so/gabang2/Elice-Mini-Project-1973c99d39354a3685e66ef5df0650b6)

### 각 TIL 링크

- [[ocr #1] Fast API PostgreSQL 환경 구축 & CRUD](https://www.notion.so/gabang2/elice-1-Fast-API-PostgreSQL-CRUD-3dce6a6a243f4c539ef06a842d1a824b)
- [[ocr #3] ERD 설계 & CRUD](https://www.notion.so/gabang2/elice-3-ERD-CRUD-fc7a6a0e768f4692848ac1697ee684c4)
- [[ocr #3] 디렉터리 구조화](https://www.notion.so/gabang2/elice-3-c9a18a905bd84e0dabcfbd4b7806db3e)
- [[ocr #3] Test Code 작성하기](https://www.notion.so/gabang2/elice-3-Test-Code-09f1666bcd6d4f23a3912a7c0b1a09fb)
- [[ocr #7] 비밀번호 암호화 관련 라이브러리 오류](https://www.notion.so/gabang2/elice-7-473cf400134f41fdb341080eebfce01e)
- [[ocr #7] JWT 검증 로직 추가](https://www.notion.so/gabang2/elice-7-JWT-bf8bfff659064c6fbbcf7826b76ec057)
- [[ocr #8] pagination 기능](https://www.notion.so/gabang2/elice-8-pagination-d31e74bd3f1248de98f0ddea41f10c7c)
- [[ocr #10] 데이터베이스 Alembic 도입 과정](https://www.notion.so/gabang2/elice-10-Alembic-734a2bcd2f1240bea7aed89c48da7299)
- [[ocr #11] docker-compose 적용하기 ](https://www.notion.so/gabang2/elice-11-docker-compose-ddbf076bc0364104bb385fc978f62c9a)