from time import time, mktime
from datetime import datetime
from base64 import b64encode
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.template.context_processors import csrf

from conf import app_base
from core.models import *
from core.utils import *


def register(rq):
	if rq.method == "GET":
		context = {}
		context.update(csrf(rq))
		return syzacz_render('core/register_form.template.html', context)
	if rq.method == "POST":
		user = User()
		user.cn = rq.POST.get("cn")
		user.name = rq.POST.get("name")
		user.surname = rq.POST.get("surname")
		user.email = rq.POST.get("email")
		user.password = rq.POST.get("password")
		user.save()
		return redirect("/%s/login" % app_base)


def login(rq):
	if rq.method == "GET":
		context = {}
		context.update(csrf(rq))
		return syzacz_render('core/login_form.template.html', context)
	if rq.method == "POST":
		# WARNING! Plain-text auth using syzacz-db, this should be changed
		user = get_object_or_404(User, cn=rq.POST.get("username"))
		if user.password == rq.POST.get("password"):
			session = Session(user=user, remote=get_request_remote_ip(rq), local=get_request_local_ip(rq))
			session.save()
			return redirect("/%s/home/%s" % (app_base, session.session_hash))
		else:
			return error("Invalid userame or password.")


def logout(rq, sessid):
	if validate_sessid(sessid):
		session = get_object_or_404(Session, session_hash=sessid)
		session.active = False
		session.save()
		return redirect("/%s/login" % app_base)
	else:
		return session_expired()

def home(rq, sessid):
	if validate_sessid(sessid):
		return syzacz_render("core/home.template.html")
	else:
		return session_expired()

def test_core(rq):
	return HttpResponse("Welcome from core view!")
