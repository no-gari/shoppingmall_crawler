# 고고싱 질문, 답변, db 저장

## Requirements
django, requests, djangorestframework

- 기술 스택 : 프론트 - HTML, CSS, jQuery 백엔드 - Django, Django-Admin, Sqlite
- BeautifulSoup을 이용한 쇼핑몰 문의사항 크롤링 및 자동응답을 위한 분류를 담당했습니다.
- '질문 크롤링 하기' 버튼을 누르면 쇼핑몰의 문의 게시판의 질문들을 스크랩 해 옵니다.
- 해당 질문을 누르면 파란색의 자동응답 예시가 나타납니다. 해당 클릭 기능은 jQuery로 구현했습니다.

## 실행 방법

- django 세팅 이후 runserver 하셔서 실행시켜 주시면 됩니다.
- 이후 화면의 '실행하기' 버튼을 누르면 크롤링이 진행 됩니다.
- 화면의 '삭제하기' 버튼을 누르면 모든 데이터가 삭제됩니다.

