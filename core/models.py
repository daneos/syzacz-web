import uuid
from django.db import models
from django.core.validators import MaxValueValidator

class User(models.Model):
    id = models.AutoField(primary_key=True)
    ldap = models.CharField(max_length=100)
    cn = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return "User(id:%d, cn:%s, ldap:%s)" % (self.id, self.cn, self.ldap)


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    time_start = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remote = models.GenericIPAddressField()
    local = models.GenericIPAddressField()
    session_hash = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return "Session(id:%d, active:%s, user:%s, remote:%s, local:%s, hash:%s)" % (self.id, self.active, self.user, self.remote, self.local, str(self.session_hash))

class Placement(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=32)
    rack_id = models.CharField(max_length=32)
    additinal_information = models.CharField(max_length=512)

class Resources (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    remained = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
    remained_alarm = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])

class Tool(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=512)
    isAble = models.BooleanField(default=True)
    lentPermission = models.BooleanField(default=True)
    memberId = models.ForeignKey('User')
    placementId = models.ForeignKey('Placement')

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)

    def __str__(self):
        return "Log(id: %d, timestamp:%s, message:%s)" % (self.id, self.timestamp, self.message)
