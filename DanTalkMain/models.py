from django.db import models
# Create your models here.

class User(models.Model):
    DanTalk_ID = models.CharField(max_length=50, null=True, blank=True)
    DanTalk_PW = models.CharField(max_length=50, null=True, blank=True)
    DanTalk_Name = models.CharField(max_length=50, null=True, blank=True)
    DanTalk_Birth = models.CharField(max_length=8, null=True, blank=True)
    DanTalk_Email = models.CharField(max_length=50, null=True, blank=True)
    DanTalk_Gender = models.CharField(max_length=2, null=True, blank=True)
    DanTalk_PersonalAgree = models.CharField(max_length=2, default="1", null=True, blank=True)
    rank_list = (('1','관리자'),('2','사용자'))
    rank = models.CharField(choices=rank_list, default='2', max_length=3)
    DanTalk_SignUpDate = models.DateField(verbose_name="회원가입 날짜", null=True, blank=True)
    DanTalk_LastDate = models.DateField(verbose_name="마지막 접속 시간", null=True, blank=True)
    DanTalk_ClientAddress = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
class FriendList(models.Model):
    Have_Friend_User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Friend_ID = models.CharField(max_length=50, null=True, blank=True)

class DanTalkRoom(models.Model):
    DanTalkRoom_ID = models.CharField(max_length=10, null=True, blank=True)
    DanTalkRoom_Name = models.CharField(max_length=100, null=True, blank=True)
    DanTalkRoom_UsrList = models.CharField(max_length=50, null=True, blank=True)