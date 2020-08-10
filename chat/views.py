from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from DanTalkMain.models import * 
from DanTalkMain.views import * 
from datetime import datetime
import json, random, string
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
from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
# Create your views here.

def index(request):
    user=User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    try:
        friend_list = FriendList.objects.filter(Have_Friend_User=user)
    except:
        friend_list = "친구 없음"

    try:
        dantalkroom_list=DanTalkRoom.objects.filter(DanTalkRoom_UsrList=request.session['dantalk_id'])
    except:
        dantalkroom_list = "대화방 없음"

    return render(request, 'chat/index.html', {'dantalkroom_list':dantalkroom_list, 'friend_list':friend_list,})

def room(request, room_name):
    user=User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)), 'usr':user, 'room_id':room_name
    })