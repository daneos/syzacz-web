import uuid
from django.db import models


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

	

class Book(models.Model):
	id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=512)
	is_able = models.BooleanField(default=True)
	lent_permission = models.BooleanField(default=True)
	member_id = models.ForeignKey('User')
	placement_id = models.ForeignKey('Placement')

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


class Log(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length=200)

	def __str__(self):
		return "Log(id: %d, timestamp:%s, message:%s)" % (self.id, self.timestamp, self.message)
