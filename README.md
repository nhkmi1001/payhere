# payhere
페이히어 Django 백엔드 과제 전형

기간 : 23/01/19 ~ 23/01/22 (4일)

## Intro
 - 회원가입과 JWT를 이용한 로그인
 - 가게부 CRUD와 복제, 단축URL을 이용한 공유 


<details>
<summary>ERD</summary>
<div markdown="1">

![image](https://user-images.githubusercontent.com/103415295/213877628-7910296b-413d-41b0-8de4-a41e66690837.png)

</div>
</details>

<details>
<summary>API</summary>
<div markdown="1">
  
<br>
 
| App| 기능| Method| URL|
|----|----|----|----|
|User|회원가입|POST|/users/
|User|회원정보 수정|PUT|/users/
|User|회원탈퇴|DELETE|/users/
|User|로그인|POST|/users/api/token/
|User|로그아웃|POST|/users/logout/
|Account|가게부 전체 리스트|GET|/account/<int:user_id>/
|Account|가게부 작성|POST|/account/<int:user_id>/
|Account|가게부 상세보기|GET|/account/<int:user_id>/<int:record_id>/
|Account|가게부 수정|PUT|/account/<int:user_id>/<int:record_id>/
|Account|가게부 삭제|DELETE|/account/<int:user_id>/<int:record_id>/
|Account|가게부 복제|POST|/account/<int:user_id>/<int:record_id>/copy/
|Account|가게부 삭제|DELETE|/account/<int:user_id>/<int:record_id>/
|Account|가게부 공유 리스트|GET|/account/<int:record_id>/share/
|Account|가게부 공유|POST|/account/<int:record_id>/share/
|Account|가게부 공유 일괄 삭제|DELETE|/account/<int:record_id>/share/
|Account|가게부 공유 유효기간 체크|GET|/account/share/<int:url_id>/
|Account|가게부 공유 삭제|DELETE|/account/share/<int:url_id>/
  
<br>
</div>
</details>

  
  ## 요구 사항 내용 및 설명
  ### 1. 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.
  - JWT토큰을 활용해 구현
  ### 2. 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다. 
  - 추가적인 회원 탈퇴 구현
  ### 3. 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다. 
  - a. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
    - User테이블과 1:M 관계 형성
  - b. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
    - serializer할 때 partial=True 를 통해 각 각 내용 수정 가능.
  - c. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
  - d. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
  - e. 가계부에서 상세한 세부 내역을 볼 수 있습니다. 
  - f. 가계부의 세부 내역을 복제할 수 있습니다.
    -  복제할 때 id=None 하고 save시킴.
  - g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    - 기존 URL을 생성하고 단축 URL을 생성. 
    - 공유 내용 일괄 삭제 구현.
  
  ### 4. 테스트 코드
  - 성공케이스/실패케이스 위주로 구현.(실패케이스 추가 필요)



