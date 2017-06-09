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


class Book(models.Model):
	id = models.AutoField(primary_key=True)
	description = models.CharField(max_length=512)
	is_able = models.BooleanField(default=True)
	lent_permission = models.BooleanField(default=True)
	member_id = models.ForeignKey('User')
	placement_id = models.ForeignKey('Placement')

	def __str__(self):
		return "Placement(id:%d, room_name:%s, rack_id:%s, additional_information:%s)" % (
		self.id, self.room_name, self.rack_id, self.additinal_information)


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

	def __str__(self):
		return "Placement(id:%d, room_name:%s, rack_id:%s, additional_information:%s)" % (self.id, self.room_name, self.rack_id, self.additinal_information)

class Resource(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	remained = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
	remained_alarm = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])

	def __str__(self):
		return "Resource(id:%d, name:%s, description:%s, remained:%d, remained_alarm:%d)" % (self.id, self.name, self.description, self.remained, self.remained_alarm)

class Resource_using(models.Model):
	id = models.AutoField(primary_key=True)
	use_date = models.DateTimeField(auto_now_add=True)
	amount = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
	comment = models.CharField(max_length=256)
	member_id = models.ForeignKey('User')
	resource_id = models.ForeignKey('Resource')

	def __str__(self):
		return "Resource_using(id:%d, use_date:%s, amount:%d, comment:%s, member_id:%d, resource_id:%d)" % (self.id, self.use_date, self.amount, self.comment, self.member_id, self.resource_id)

class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=512)
	available = models.BooleanField(default=True)
	lent_permission = models.BooleanField(default=True)
	member_id = models.ForeignKey('User')
	placement_id = models.ForeignKey('Placement')

	def __str__(self):
		return "Tool(id:%d, description:..., is_able:%s, lent_permission:%s, member_id:%s, placement_id:%s)" % (self.id, self.available, self.lent_permission, self.member_id, self.placement_id)

class Lent(models.Model):
	id = models.AutoField(primary_key=True)
	lent_date = models.DateTimeField(auto_now_add=True)
	planned_return_date = models.DateTimeField()
	return_date = models.DateTimeField(null=True)
	comment = models.CharField(max_length=256)
	member_id = models.ForeignKey('User')
	tool_id = models.ForeignKey('Tool')

	def __str__(self):
		return "Lent(id:%d, lent_date:%s, planned_return_date:%s, return_date:%s, comment:%s ,member_id:%s, placement_id:%s)" % (self.id, self.lent_date, self.planned_return_date, self.return_date,self.comment, self.member_id, self.tool_id)

class Lent_form(models.Model):
	id = models.AutoField(primary_key=True)
	lent_date = models.DateTimeField(auto_now_add=True)
	planned_return_date = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=256)
	permission = models.BooleanField(default=False)
	member_id = models.ForeignKey('User')
	tool_id = models.ForeignKey('Tool')

	def __str__(self):
		return "Lent_form(id:%d, lent_date:%s, planned_return_date:%s, comment:%s , permission:%s, member_id:%d, tool_id:%d)" % (self.id, self.lent_date, self.planned_return_date,self.comment, self.member_id, self.tool_id)


class Priority(models.Model):
	id = models.AutoField(primary_key=True)
	priority_name = models.CharField(max_length=32)
	priority_level = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])

	def __str__(self):
		return "Priority(id:%d, priority_name:%s, priority_level:%d)" % (self.id, self.priority_name, self.priority_level)

class Notification(models.Model):
	id = models.AutoField(primary_key=True)
	user_priority = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
	description = models.CharField(max_length=512)
	member_id = models.ForeignKey('User')
	priority_id = models.ForeignKey('Priority')

	def __str__(self):
		return "Notification(id: %d, user_priority:%d, description:%s, member_id:%s, priority_id:%s)" % (self.id, self.user_priority, self.description, self.member_id, self.priority_id)

class Special_function(models.Model):
	id = models.AutoField(primary_key=True)
	function_name = models.CharField(max_length=32)

	def __str__(self):
		return "Special_function(id:%d, function_name:%s)" % (self.id, self.function_name)

class Members_special_function(models.Model):
	member_id = models.ForeignKey('User')
	priority_id = models.ForeignKey('Special_function')

	def __str__(self):
		return "Members_special_function(member_id:%d, priority_id:%d)" % (self.id, self.function_name)



class Log(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length=200)

	def __str__(self):
		return "Log(id: %d, timestamp:%s, message:%s, member_id:%s)" % (self.id, self.timestamp, self.message, self.member_id)
