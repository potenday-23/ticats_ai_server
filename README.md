# 엘리스 미니 프로젝트
엘리스 신입(python) 채용 과제로 수행한, 게시판, 게시글을 작성할 수 있는 FastAPI 기반 프로젝트<br>
✔ 배포 웹사이트 : http://54.180.102.238:8080/docs <br>
✔ 수행 기간 : 2023.12.01(9:00) ~ 2023.12.05(9:00)<br>
✔ Tech : FastAPI, SQLAlchemy, pydantic, postgresql, JWT, Alembic, Docker, AWS<br>

![image](https://github.com/gabang2/elice_mini_project/assets/82714785/4aa8f5c9-35de-4327-90c0-339c24688411)

## Summary
- 계정 회원가입(Signup), 로그인(Login), 로그아웃(Logout)
- 게시판 생성, 수정(내 게시판만), 삭제(내 게시판만), 조회(내 게시판, 전체공개 게시판), List(내 게시판, 전체공개 게시판)
- 게시글 생성, 수정(내 게시글만), 삭제(내 게시글만), 조회(내 게시판, 전체공개 게시판의 게시글), List(내 게시판, 전체공개 게시판의 게시글)

## Skils
언어 및 프레임워크: ![Static Badge](https://img.shields.io/badge/Python-3.10-Blue) ![Static Badge](https://img.shields.io/badge/FastAPI-0.104.1-Blue)<br/>
데이터베이스 및 테스트: ![Static Badge](https://img.shields.io/badge/PostgreSQL-13-Green) ![Static Badge](https://img.shields.io/badge/Pytest-7.4.3-Pink) <br/>
배포 : ![Static Badge](https://img.shields.io/badge/Linux-Red) ![Static Badge](https://img.shields.io/badge/AWS-Orange)![Static Badge](https://img.shields.io/badge/Docker-Blue) <br/>

## Installation
1. 환경변수 설정
   ```env
   SQLALCHEMY_DATABASE_URL=postgresql://postgres:admin1234@127.0.0.1:5432/postgres
   SECRET_KEY=e068f0399d3729db42eafdc56ca258ff3954c38a24ac423a6d5b15005378785c
   REDIS_HOST=localhost
   ```
2. 라이브러리 설치
   ```bash
      pip install requirements.txt
   ```
3. 엘리스 미니 프로젝트 실행
    ```bash
   alembic upgrade head
   uvicorn main:app --reload
    ```
## 디렉터리 구조
- 3-Tier Architecture 방식 적용
- 관련 TIL : [[elice #3] 디렉터리 구조화](https://www.notion.so/gabang2/elice-3-c9a18a905bd84e0dabcfbd4b7806db3e)

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
엘리스 미니 프로젝트 Test
=> tests 폴더 Run
> ![image](https://github.com/gabang2/elice_mini_project/assets/82714785/eeb3c59c-a25c-4437-9a0e-4c8571598bdc)
 ![Static Badge](https://img.shields.io/badge/Test_Passed-4/5-green)<br/>

## API 문서
![image](https://github.com/gabang2/elice_mini_project/assets/82714785/4324a516-ee70-4be5-8858-1e9f5c353689)
[API 문서 바로가기👈](http://54.180.102.238:8080/docs#/)

## 프로젝트 진행 관리
- Github의 Project 기능을 통해 예정 기간 및 완료 여부 관리
![image](https://github.com/gabang2/elice_mini_project/assets/82714785/d444f680-043f-4c56-8cf4-0b82bc55dc87)<br>
[![Github Project](https://img.shields.io/badge/Github-%23000000.svg?style=for-the-badge&logo=Github&logoColor=white)](https://github.com/users/gabang2/projects/1/views/2)

## 설계
- E-R Diargram
  ![image](https://github.com/gabang2/elice_mini_project/assets/82714785/043279ba-2cfe-4bc1-840e-3b805c47878b)
<br>
- Architecture<br>


  ![image](https://github.com/gabang2/elice_mini_project/assets/82714785/9011fff4-2492-4e2e-a0a1-f7dc275d5fc5)




## TIL
### 전체 TIL 링크
- [Elice Mini Project](https://www.notion.so/gabang2/Elice-Mini-Project-1973c99d39354a3685e66ef5df0650b6)
### 각 TIL 링크
- [[elice #1] Fast API PostgreSQL 환경 구축 & CRUD](https://www.notion.so/gabang2/elice-1-Fast-API-PostgreSQL-CRUD-3dce6a6a243f4c539ef06a842d1a824b)
- [[elice #3] ERD 설계 & CRUD](https://www.notion.so/gabang2/elice-3-ERD-CRUD-fc7a6a0e768f4692848ac1697ee684c4)
- [[elice #3] 디렉터리 구조화](https://www.notion.so/gabang2/elice-3-c9a18a905bd84e0dabcfbd4b7806db3e)
- [[elice #3] Test Code 작성하기](https://www.notion.so/gabang2/elice-3-Test-Code-09f1666bcd6d4f23a3912a7c0b1a09fb)
- [[elice #7] 비밀번호 암호화 관련 라이브러리 오류](https://www.notion.so/gabang2/elice-7-473cf400134f41fdb341080eebfce01e)
- [[elice #7] JWT 검증 로직 추가](https://www.notion.so/gabang2/elice-7-JWT-bf8bfff659064c6fbbcf7826b76ec057)
- [[elice #8] pagination 기능](https://www.notion.so/gabang2/elice-8-pagination-d31e74bd3f1248de98f0ddea41f10c7c)
- [[elice #10] 데이터베이스 Alembic 도입 과정](https://www.notion.so/gabang2/elice-10-Alembic-734a2bcd2f1240bea7aed89c48da7299)
- [[elice #11] docker-compose 적용하기 ](https://www.notion.so/gabang2/elice-11-docker-compose-ddbf076bc0364104bb385fc978f62c9a)