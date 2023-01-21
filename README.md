# payhere
페이히어 Django 백엔드 과제 전형

기간 : 23/01/19 ~ 23/01/22 (4일)

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
  




