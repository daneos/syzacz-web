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


# def register(rq):
# 	event = "0001 User registered"
# 	try:
# 		user = User(
# 			name=rq.GET.get("name"),
# 			surname=rq.GET.get("surname"),
# 			address=rq.GET.get("address"),
# 			phone=rq.GET.get("phone"),
# 			email=rq.GET.get("email"),
# 			password=rq.GET.get("p")
# 		)
# 		user.save()
# 	except Exception:
# 		return response("error", "9003 Not registered")
# 	else:
# 		return response("ok", IdSerializer(event, user))


def login(rq):
	if rq.method == "GET":
		next_url = rq.GET.get("next")
		context = {}
		if next_url:
			context["next"] = next_url
		context.update(csrf(rq))
		return syzacz_render('core/login_form.template.html', context)
	if rq.method == "POST":
		# WARNING! Plain-text auth using syzacz-db, this should be changed
		user = get_object_or_404(User, cn=rq.POST.get("username"))
		if user.password == rq.POST.get("password"):
			session = Session(user=user, remote=get_request_remote_ip(rq), local=get_request_local_ip(rq))
			session.save()
			next_url = rq.GET.get("next")
			print next_url
			response = redirect(next_url or "/%s/home" % app_base)
			response.set_cookie("syzacz_sessid", session.session_hash)
			return response
		else:
			return error("Invalid userame or password.")


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
		return syzacz_render("core/home.template.html")
	else:
		return session_expired("/%s/home" % app_base)

def test_core(rq):
	return HttpResponse("Welcome from core view!")
