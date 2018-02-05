from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.shortcuts import redirect

from conf import app_base
from core.version import Version

env = {}


def init(plugin_env):
    global env
    env = plugin_env
    return Version([0, 1, 0, "alpha"])


def urls():
	return[
		["%s/users/$", "users", None],
		["%s/users_m/$", "users_list_m", "user/users_manage.template.html"],
		["%s/users_s/$", "users_list_s", "user/users_show.template.html"],
        ["%s/user.show/(?P<user_id>[0-9]+)/$", "user_show", "user/user_data.template.html"],
		["%s/user.rfid_state/(?P<rfid_id>[0-9a-zA-Z]+)/$", "rfid_state", None],
		["%s/user.role/(?P<user_id>[0-9]+)/$", "grant_access", "user/grant.template.html"]
        #["%s/account.delete_session/(?P<session_id>[0-9]+)/$", "delete_session", None],
        #["%s/account.change_email$", "change_email", None],
        #["%s/account.change_password$", "change_password", None],
        #["%s/account.settings", "account_settings", "account/settings.template.html"]
    ]

def users(rq):
	User = env["getModel"]("User")
	Session = env["getModel"]("Session")
	
	session = Session.objects.get(session_hash=env["sessid"](rq))
	user=session.user
	if user.role == 1:
		return redirect("/%s/users_m/" % app_base)
	return redirect("/%s/users_s/" % app_base)
	
def users_list_m(rq):
	User = env["getModel"]("User")
	Session = env["getModel"]("Session")
	
	session = Session.objects.get(session_hash=env["sessid"](rq))
	user=session.user
	if user.role != 1:
		return redirect("/%s/users_s/" % app_base)
	try:
		users = User.objects.all()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}
	return {"users": users}

def users_list_s(rq):
	User = env["getModel"]("User")
	Session = env["getModel"]("Session")
	
	session = Session.objects.get(session_hash=env["sessid"](rq))
	user=session.user
	try:
		users = User.objects.all()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}
	return {"users": users}
	
def user_show(rq, user_id):
	Session = env["getModel"]("Session")
	User = env["getModel"]("User")
	Rfid = env["getModel"]("Rfid")
	session = Session.objects.get(session_hash=env["sessid"](rq))
	suser = User.objects.get(id=user_id)
	currentUser = session.user
	rfids = Rfid.objects.filter(user = suser)
	if suser:
		if currentUser.role == 1:
			return {"suser" : suser, "rfids" : rfids}
	return HttpResponseNotFound('<h1>No Page Here</h1>')
	
def rfid_state(rq, rfid_id):
	Session = env["getModel"]("Session")
	User = env["getModel"]("User")
	Rfid = env["getModel"]("Rfid")
	rfid = Rfid.objects.get(id = rfid_id)
	suser = rfid.user
	try:
		session = Session.objects.get(session_hash=env["sessid"](rq))
	except Exception as e:
		return redirect("/%s/user.show/%s/?error=%s" % (app_base, suser.id, str(e)))
	if rfid.active is True:
		rfid.active = False
	else:
		rfid.active = True
	rfid.save()
	return redirect("/%s/user.show/%s/?msg=Rfid updated" % (app_base, suser.id))
		
def grant_access(rq, user_id):
	Session = env["getModel"]("Session")
	User = env["getModel"]("User")
	session = Session.objects.get(session_hash=env["sessid"](rq))
	admin = session.user
	suser = User.objects.get(id=user_id)
	if rq.method == "GET":
		if suser:
			if admin.role == 1:
				context = {"suser" : suser}
				context.update(env["csrf"](rq))
				return context
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	
	if rq.method == "POST":
		if suser:
			if admin.role == 1:
				try:
					suser.role = rq.POST.get("role")
					suser.save()
				except Error as e:
					return {"error": "Cannot add new object: %s" % e}
				return redirect("/%s/user.show/%s/?msg=Role updated" % (app_base, suser.id))
		return HttpResponseNotFound('<h1>No Page Here</h1>')
			