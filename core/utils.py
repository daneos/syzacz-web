import json
from datetime import datetime
from time import time
from uuid import uuid4

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from conf import app_base
from core.models import *

def syzacz_render(template, context={}):
	context.update({"app_base":app_base})
	return render_to_response(template, context)

def validate_sessid(sessid):
	session = get_object_or_404(Session, session_hash=sessid)
	print "[CHECK] %s" % str(session)
	if session.active:
		session.last_activity = datetime.now()
		session.save()
	return session.active

def error(message):
	return syzacz_render("core/error.template.html", {"error": message})

def session_expired():
	return error("Session expired.")

def get_request_remote_ip(rq):
	x_forwarded_for = rq.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		return x_forwarded_for.split(',')[-1].strip()
	else:
		return rq.META.get('REMOTE_ADDR')

def get_request_local_ip(rq):
	return "127.0.0.1"