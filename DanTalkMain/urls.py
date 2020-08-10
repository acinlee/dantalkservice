from . import views
from chat.views import index
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'DanTalkMain'

urlpatterns = [
    path('', views.main, name='main'),
    path('DanTalk/loginpage', views.loginpage, name='loginpage'),
    path('DanTalk/login', views.login, name="login"),
    path('DanTalk/toSignUp', views.toSignUp, name="toSignUp"),
    path('DanTalk/SignUp', views.SignUp, name="SignUp"),
    path('DanTalk/logout', views.logout, name="logout"),
    path('DanTalk/find_userinfo_id', views.find_userinfo_id, name="find_userinfo_id"),
    path('DanTalk/find_userinfo_pw', views.find_userinfo_pw, name="find_userinfo_pw"),
    path('DanTalk/to_usr_pw_modify', views.to_usr_pw_modify, name="to_usr_pw_modify"),
    path('DanTalk/usr_pw_modify', views.usr_pw_modify, name="usr_pw_modify"),

    path('DanTalk/to_add_friend_list', views.to_add_friend_list, name="to_add_friend_list"),

    path('DanTalk/to_add_talkroom_list', views.to_add_talkroom_list, name="to_add_talkroom_list"),
    path('DanTalk/connectDanTalk/<dantalk_num>', views.connectDanTalk, name="connectDanTalk"),
    path('DanTalk/admin_main', views.admin_main, name="admin_main"),
    path('DanTalk/to_usr_pw_modify_admin/<usr_id>', views.to_usr_pw_modify_admin, name="to_usr_pw_modify_admin"),
    path('DanTalk/usr_pw_modify_admin/<usr_id>', views.usr_pw_modify_admin, name="usr_pw_modify_admin"),

    #회원가입 완료
    path('DanTalk/SignUpGo', views.SignUpGo, name='SignUpGo'),

    #이메일
    path('DanTalk/activate/<uid64>/<token>', views.activate, name='activate'),
    path('DanTalk/findID', views.find_id, name='find_id'), #아이디 찾기 메일
    path('DanTalk/findPW', views.find_pw, name='find_pw'), #비밀번호 찾기 메일

    #chat
    path('chat/', index, name='index'), 

    #ajax
    path('SignUp_idcheck', views.SignUp_idcheck, name='SignUp_idcheck'), #user id 중복 확인
    path('SignUp_emailcheck', views.SignUp_emailcheck, name='SignUp_emailcheck'), #회원 가입시 이메일 중복 방지
    path('ajax/findfriend', views.findFriend, name="findFriend"), #유저 id 찾기
    path('ajax/friendAdd', views.friendAdd, name="friendAdd"), 
    path('ajax/friendDelete', views.friendDelete, name="friendDelete"), 
    path('ajax/dantalkAdd', views.dantalkAdd, name="dantalkAdd"), 
    path('ajax/dantalkDelete', views.dantalkDelete, name="dantalkDelete"),
    path('ajax/usrDelete', views.usrDelete, name="usrDelete"),
    
    #path('Usrmodify_emailcheck', views.Usrmodify_emailcheck, name='Usrmodify_emailcheck'), #회원 정보 수정시 이메일 중복 방지
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)