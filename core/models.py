import uuid
from django.db import models
from django.core.validators import MaxValueValidator
from datetime import datetime, timedelta


def user_validity(days):
	validity_date = datetime.now() + timedelta(days=days)
	return validity_date


class User(models.Model):
	ROLE_CHOICES= (
                (1, 'Admin'),
                (2, 'Active'),
                (3, 'Unactive'),
                (4, 'Blocked'),
                (5, 'Registered'),
                )
	
	id = models.AutoField(primary_key=True)
	ldap = models.CharField(max_length=100)
	cn = models.CharField(max_length=50)
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=128)
	validity = models.DateTimeField(default=user_validity(365))
        role = models.PositiveIntegerField(choices=ROLE_CHOICES, default=5)

	def __str__(self):
		return "User(id:%d, cn:%s, ldap:%s)" % (self.id, self.cn, self.ldap)


class Invoice(models.Model):
        id = models.AutoField(primary_key=True)
	invoice_number = models.CharField(max_length=32)
	permalink = models.CharField(max_length=256)
	issue_date = models.DateTimeField()
	add_date = models.DateTimeField(auto_now_add=True)
	amount = models.DecimalField(decimal_places=2, max_digits=10)
	with_cashbacked = models.NullBooleanField(null=True)
	cashbacked = models.BooleanField(default=False)
	posted = models.NullBooleanField(null=True)
	group = models.CharField(null=True, max_length=16)
	description = models.CharField(max_length=256)
	member_id = models.ForeignKey('User')
	file = models.FileField(upload_to="storage/syzacz/faktury", null=True)

	def __str__(self):
		return ("Invoice(id:%d, permalink:%s, issue_date:%s, add_date:%s, amount:%s, with_cashbacked:%s,"+
		"cashbacked:%s, posted:%s, description:%s, member_id:%s)") % (
		self.id, self.permalink, self.issue_date, self.add_date, self.amount, self.with_cashbacked,
		self.cashbacked, self.posted, self.description, self.member_id)


class Book(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=512, default="")
	pages = models.IntegerField(default=1)
	description = models.CharField(max_length=512)
	available = models.BooleanField(default=True)
	review = models.CharField(max_length=4096, default="Brak")
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
	amount = models.PositiveIntegerField()
	alarm = models.PositiveIntegerField()

	def __str__(self):
		return "Resource(id:%d, name:%s, description:%s, amount:%d, alarm:%d)" % (self.id, self.name, self.description, self.amount, self.alarm)

	def is_alarm(self):
		return self.amount <= self.alarm

	def use(self, amount):
		self.amount -= amount

	def refill(self, amount):
		self.amount += amount


class ResourceUsage(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateTimeField(auto_now_add=True)
	member = models.ForeignKey('User')
	amount = models.PositiveIntegerField()
	comment = models.CharField(max_length=256)
	resource = models.ForeignKey('Resource')

	def __str__(self):
		return "ResourceUsage(id:%d, date:%s, amount:%d, comment:%s, member:%s, resource:%s)" % (self.id, self.date, self.amount, self.comment, self.member, self.resource)


class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=512)
	available = models.BooleanField(default=True)
	lend_permission = models.BooleanField()
	member = models.ForeignKey('User')
	placement = models.ForeignKey('Placement')

	def __str__(self):
		return "Tool(id:%d, description:..., is_able:%s, lent_permission:%s, member_id:%s, placement_id:%s)" % (self.id, self.available, self.lend_permission, self.member_id, self.placement_id)


class Lent(models.Model):
	id = models.AutoField(primary_key=True)
	lent_date = models.DateTimeField(auto_now_add=True)
	planned_return_date = models.DateTimeField()
	return_date = models.DateTimeField(null=True)
	comment = models.CharField(max_length=256)
	member = models.ForeignKey('User')
	tool = models.ForeignKey('Tool', null=True)
	book = models.ForeignKey('Book', null=True)

	def __str__(self):
		return "Lent(id:%d, lent_date:%s, planned_return_date:%s, return_date:%s, comment:%s ,member_id:%s, placement_id:%s)" % (self.id, self.lent_date, self.planned_return_date, self.return_date,self.comment, self.member_id, self.tool_id)


class Priority(models.Model):
	id = models.AutoField(primary_key=True)
	priority_name = models.CharField(max_length=32)
	priority_level = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])

	def __str__(self):
		return "Priority(id:%d, priority_name:%s, priority_level:%d)" % (self.id, self.priority_name, self.priority_level)

class Notification(models.Model):
	STATUS_CHOICES =(
                (1, 'Nowy'),
                (2, 'Zablokowane'),
                (3, 'On going'),
                (4, 'Rozwiazane'),
                )
        id = models.AutoField(primary_key=True)
	user_priority = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
	description = models.CharField(max_length=512)
	member_id = models.ForeignKey('User')
	priority_id = models.ForeignKey('Priority')
        status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)

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
		return "Log(id: %d, timestamp:%s, message:%s)" % (self.id, self.timestamp, self.message)
