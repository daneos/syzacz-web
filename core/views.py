# from time import time, mktime
from datetime import datetime
# from base64 import b64encode
from django.shortcuts import get_object_or_404, redirect
# from django.db.models import Q
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from conf import app_base, plugin_blacklist, version
from core.models import *
from core.utils import *
from core.log import log


def start(rq):
	log("[START] Started at %s" % str(datetime.today()))
	return HttpResponse("syzacz-web %s [HSKRK]" % str(version))


def landing(rq):
	if validate_sessid(rq):
		return redirect("/%s/home" % app_base)
	else:
		return redirect("/%s/login" % app_base)


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


def _login_form(rq, context, next_url=None):
	if next_url:
		context["next"] = next_url
	context.update(csrf(rq))
	return syzacz_render('core/login_form.template.html', context)


def login(rq):
	next_url = rq.GET.get("next")

	if validate_sessid(rq):
		return redirect("/%s/home" % app_base)

	if rq.method == "GET":
		return _login_form(rq, {}, next_url)

	if rq.method == "POST":
		try:
			user = User.objects.get(cn=rq.POST.get("username"))
		except ObjectDoesNotExist:
			user = None

		if user:
			# WARNING! Plain-text auth using syzacz-db, this should be changed
			if user.password == rq.POST.get("password"):
				session = Session(user=user, remote=get_request_remote_ip(rq), local=get_request_local_ip(rq))
				session.save()
				response = redirect(next_url or "/%s/home" % app_base)
				response.set_cookie("syzacz_sessid", session.session_hash)
				return response
		return _login_form(rq, { "error": "Invalid user name or password" }, next_url)


def logout(rq):
	if validate_sessid(rq):
		session = get_object_or_404(Session, session_hash=sessid(rq))
		session.active = False
		session.save()
		return redirect("/%s/login" % app_base)
	else:
		return session_expired()


def home(rq):
	if validate_sessid(rq):
		session = get_object_or_404(Session, session_hash=sessid(rq))
		context = {"user": session.user, "plugin_blacklist": plugin_blacklist}
		return syzacz_render("core/home.template.html", context)
	else:
		return session_expired("/%s/home" % app_base)


def test_core(rq):
	return HttpResponse("Welcome from core view!")
