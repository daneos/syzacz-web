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
        ["%s/user.show/(?P<user_id>[0-9]+)/$", "user_show", "user/user_data.template.html"]
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
	
