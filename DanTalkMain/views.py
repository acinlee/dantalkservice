from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from datetime import datetime
import json, random, string
from .forms import *
from django.utils import timezone
from django.utils.encoding import smart_text
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#이메일 관련 import
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import AccountActivationTokenGenerator
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
# Create your views here.

#메인 페이지
def main(request):
    return render(request, 'DanTalkMain/main/main.html')

# 세션 관리s
def addSessions(request, user):
    request.session['dantalk_id'] = user.DanTalk_ID
    request.session['dantalk_pw'] = user.DanTalk_Name
    request.session['rank'] = user.rank

# 접속자의 유저 객체 반환
def getInfo(request):
    user = User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    return user

#로그인 페이지
def loginpage(request):
    return render(request, 'DanTalkMain/login/loginpage.html')

# 로그인
def login(request):
    if request.method == 'POST':
        user_id = request.POST['dantalk_id']
        user_pw = request.POST['dantalk_pw']
        try:
            user = User.objects.get(DanTalk_ID=user_id)
            if ((user.rank == '1' or user.rank == '2') and user_pw == user.DanTalk_PW and user.is_active==True):
                addSessions(request, user)    
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                User.objects.filter(DanTalk_ID=user_id).update(
                    DanTalk_ClientAddress = ip
                )
                return render(request, 'DanTalkMain/main/main.html', {
                    'user_info' : user,
                    })
            elif user_pw != user.DanTalk_PW:
                return render_to_response('DanTalkMain/error/error.html', {
                    'alert_msg' : '비밀번호가 맞지 않습니다.',
                    'url' : '/'
                })
            else:
                return render_to_response('DanTalkMain/error/error.html', {
                    'alert_msg' : '이메일 인증이 완료되지 않았습니다.',
                    'url' : '/'
                })
                #raise (Http404("비밀번호가 맞지 않습니다."))
        except User.DoesNotExist:
            return render_to_response('DanTalkMain/error/error.html', {
                    'alert_msg' : '해당 아이디가 없습니다.',
                    'url' : '/'
                })
    else:
        return render(request, 'DanTalkMain/login/loginpage.html', {
            'user_info' : getInfo(request),
             })

# 로그아웃 클릭 시
def logout(request):
    for item in list(request.session.keys()):
        del request.session[item]

    return render(request, 'DanTalkMain/main/main.html')

#아이디, 비밀번호 찾기 이동
def find_userinfo_id(request):
    return render(request, 'DanTalkMain/login/find_usr_id.html')

def find_userinfo_pw(request):
    return render(request, 'DanTalkMain/login/find_usr_pw.html')

#아이디 비밀번호 찾기 기능
def find_id(request):
    try:
        user = User.objects.get(DanTalk_Name=request.POST['find_usr_name'], DanTalk_Email=request.POST['find_usr_email'])
        message = render_to_string('DanTalkMain/login/find_usr_id_email.html',{
                'user': user,
        })
        mail_subject = "[단톡방] 아이디 찾기 메일입니다."
        user_email = user.DanTalk_Email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'DanTalkMain/login/find_usr_id_ok.html')
    except:
        messages.error(request, '해당하는 정보의 아이디가 없습니다.')
        return redirect('DanTalkMain:find_userinfo_id')
    
def find_pw(request):
    try:
        user = User.objects.get(DanTalk_Name=request.POST['find_usr_name'], DanTalk_ID=request.POST['find_usr_id'], DanTalk_Email=request.POST['find_usr_email'])
        
        _LENGTH = 12 # 12자리

        # 숫자 + 대소문자
        string_pool = string.ascii_letters + string.digits
        # 랜덤한 문자열 생성
        update_usr_pw = "" 
        
        for i in range(_LENGTH) :
            update_usr_pw += random.choice(string_pool) # 랜덤한 문자열 하나 선택
        
        User.objects.filter(DanTalk_Name=request.POST['find_usr_name']).filter(DanTalk_ID=request.POST['find_usr_id']).filter(DanTalk_Email=request.POST['find_usr_email']).update(
            DanTalk_PW = update_usr_pw,
        )
        message = render_to_string('DanTalkMain/login/find_usr_pw_email.html', {
            'user_pw':update_usr_pw,
        })
        mail_subject = "[단톡방] 임시 비밀번호 메일입니다."
        user_email = user.DanTalk_Email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'DanTalkMain/login/find_usr_pw_ok.html')
    except:
        messages.error(request, '해당하는 정보의 회원이 없습니다.')
        return redirect('DanTalkMain:find_userinfo_pw')


#회원 가입 페이지 이동
def toSignUp(request):
    user = User.objects.all()
    return render(request, 'DanTalkMain/signup/signup.html', {'user_info':user})

#회원 가입
def SignUp(request):
    if request.method == "POST":
        #이메일
        email_text = request.POST['email_text']
        email_select = request.POST['email_select']
        dantalk_email = email_text+'@'+email_select
        
        #생년월일
        user_year = request.POST['usr_year']
        user_month = request.POST['usr_month']
        user_day = request.POST['usr_day']
        if len(user_day) == 1:
            user_day = '0'+user_day
        user_birth = user_year+user_month+user_day
        
        #성별
        dantalk_gendercheck = request.POST['usr_gender']
        dantalk_gender = ''
        if dantalk_gendercheck == '남자':
            dantalk_gender = '1'
        else:
            dantalk_gender = '2'
        

        user = User.objects.create(
        DanTalk_ID = request.POST['dantalk_id'],
        DanTalk_PW = request.POST['dantalk_pw'],
        DanTalk_Name = request.POST['usr_name'],
        DanTalk_Birth = user_birth,
        DanTalk_Gender = dantalk_gender,
        DanTalk_Email = dantalk_email,
        DanTalk_SignUpDate = datetime.now()
        )

        user.is_active = False
        current_site = get_current_site(request) 
        # localhost:8000
        message = render_to_string('DanTalkMain/signup/usr_active.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
        })
        mail_subject = "[단톡방] 회원가입 인증 메일입니다."
        user_email = dantalk_email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        return render(request, 'DanTalkMain/signup/emailok.html')

    return render(request, 'DanTalkMain/signup/signup.html')

def activate(request, uid64, token):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('DanTalkMain:SignUpGo')
    else:
        return HttpResponse('비정상적인 접근입니다.')

#회원가입 완료 페이지
def SignUpGo(request):
    return render(request, 'DanTalkMain/signup/signupok.html')

#회원가입시 유저 id 중복 방지
def SignUp_idcheck(request):
    id_check = request.POST['idcheck']
    UserList = User.objects.filter(DanTalk_ID=id_check)
    if not UserList:
        context = {  'msg' : 'Y',  }
    else:
        context = {  'msg' : 'N',  }

    return HttpResponse(json.dumps(context), content_type="application/json")

#회원가입시 유저 email 중복 방지
def SignUp_emailcheck(request):
    emailcontent = request.POST['emailcontent']
    emailcompany = request.POST['emailcompany']
    cdc_email = emailcontent+'@'+emailcompany
    UserList = User.objects.filter(DanTalk_Email=cdc_email)
    if not UserList:
        context = {  'msg' : 'Y',  }
    else:
        context = {  'msg' : 'N',  }

    return HttpResponse(json.dumps(context), content_type="application/json")

#회원 정보 수정 이동
def to_usr_pw_modify(request):
    return render(request, 'DanTalkMain/mypage/usr_pw_modify.html')

#회원 정보 수정
def usr_pw_modify(request):
    if request.method == "POST":
        User.objects.filter(DanTalk_ID=request.session['dantalk_id']).update(
            DanTalk_PW = request.POST['dantalk_pw']
        )
        messages.success(request, '비밀번호 변경 완료')
        return redirect('DanTalkMain:main')
    else:
        return render(request,'DanTalkMain/mypage/usr_pw_modify.html')

#친구 관리
def to_add_friend_list(request):
    user=User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    try:
        friend_list = FriendList.objects.filter(Have_Friend_User=user)
    except:
        friend_list = "친구 없음"
    return render(request, 'DanTalkMain/friend_management/add_friend.html', {'friend_list':friend_list,})

#친구 검색
def findFriend(request):
    find_content = request.POST['friend_id'] #유저가 입력한 텍스트
    user_list = User.objects.filter(DanTalk_ID__icontains=find_content).exclude(DanTalk_ID=request.session['dantalk_id']).order_by('DanTalk_ID')
    user_id_list = []
    for user in user_list:
        user_id_list.append(user.DanTalk_ID)

    if not user_id_list:
        context = {  'msg' : 'N',  }
    else:
        context = {  'msg' : 'Y', 'user_id_list':user_id_list,}

    return HttpResponse(json.dumps(context), content_type="application/json")

#친구 추가
def friendAdd(request):
    friend_id = request.POST['friend_id'] #유저가 입력한 텍스트
    user = User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    FriendList.objects.create(
        Have_Friend_User=user,
        Friend_ID=friend_id
    )
    return HttpResponse("success")

#친구 삭제
def friendDelete(request):
    friend_id = request.POST['friend_id']
    user = User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    FriendList.objects.get(Have_Friend_User=user, Friend_ID=friend_id).delete()

    return HttpResponse("success")

#대화방 관리
def to_add_talkroom_list(request):
    user=User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    try:
        friend_list = FriendList.objects.filter(Have_Friend_User=user)
    except:
        friend_list = "친구 없음"

    try:
        dantalkroom_list=DanTalkRoom.objects.filter(DanTalkRoom_UsrList=request.session['dantalk_id'])
    except:
        dantalkroom_list = "대화방 없음"

    return render(request, 'DanTalkMain/talkroom/dantalkmain.html', {'dantalkroom_list':dantalkroom_list, 'friend_list':friend_list,})

#대화방 추가
def dantalkAdd(request):
    dantalk_list = request.POST['dantalk_list']
    dantalk_name = request.POST['dantalk_name']
    dantalk_usr = dantalk_list.split(',')
    del dantalk_usr[0]
    dantalk_usr.append(request.session['dantalk_id'])
    unique_number = random.randint(0,999999)
    for a in dantalk_usr:
        DanTalkRoom.objects.create(
        DanTalkRoom_ID=unique_number,
        DanTalkRoom_Name=dantalk_name,
        DanTalkRoom_UsrList=a,
    )
    
    return HttpResponse("success")

#대화방 삭제
def dantalkDelete(request):
    friend_dantalk = request.POST['friend_dantalk']
    DanTalkRoom.objects.get(DanTalkRoom_ID=friend_dantalk, DanTalkRoom_UsrList=request.session['dantalk_id']).delete()

    return HttpResponse("success")

#대화방 접속
def connectDanTalk(request, dantalk_num):
    dantalk_object = DanTalkRoom.objects.filter(DanTalkRoom_ID=dantalk_num)

    return render(request, 'DanTalkMain/talkroom/dantalkroom.html', {'dantalk_object':dantalk_object})

#관리자
def admin_main(request):
    user_list = User.objects.all()
    dantalkroom_list = DanTalkRoom.objects.all()
    usr_count = 0
    talk_count = 0
    for a in user_list:
        usr_count = usr_count+1
    for a in dantalkroom_list:
        talk_count = talk_count+1

    return render(request, 'DanTalkMain/dantalkadmin/adminmain.html', {'dantalkroom_list':dantalkroom_list, 'user_list':user_list, 'usr_count':usr_count,'talk_count':talk_count})

#친구 삭제
def usrDelete(request):
    friend_id = request.POST['friend_id']
    
    User.objects.get(DanTalk_ID=friend_id).delete()

    return HttpResponse("success")

#회원 정보 수정 이동
def to_usr_pw_modify_admin(request, usr_id):
    user_id = usr_id
    return render(request, 'DanTalkMain/dantalkadmin/usr_modify.html',{'user_id':user_id})

#회원 정보 수정
def usr_pw_modify_admin(request, usr_id):
    if request.method == "POST":
        User.objects.filter(DanTalk_ID=usr_id).update(
            DanTalk_PW = request.POST['dantalk_pw']
        )
        messages.success(request, '비밀번호 변경 완료')
        return redirect('DanTalkMain:main')
    else:
        return render(request,'DanTalkMain/dantalkadmin/adminmain.html')

