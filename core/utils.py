# import json
import socket
from datetime import datetime
from ast import literal_eval
# from time import time
# from uuid import uuid4

# from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaulttags import register

from conf import app_base
from core.models import *
from core.log import log


def syzacz_render(template, context={}):
	log("[RENDER] %s" % template)
	context.update({"app_base": app_base})
	return render_to_response(template, context)


def validate_sessid(rq):
	try:
		session = Session.objects.get(session_hash=sessid(rq))
	except ObjectDoesNotExist:
		log("[CHECK] Non-existent sessid:%s" % sessid(rq))
		return False
	log("[CHECK] %s" % str(session))
	if session:
		if session.active:
			session.last_activity = datetime.now()
			session.save()
		return session.active
	else:
		return False


def sessid(rq):
	return rq.COOKIES.get("syzacz_sessid")


def error(message):
	return syzacz_render("core/error.template.html", {"error": message})


def session_expired(url=""):
	if url:
		url = "?next=%s" % url
	return redirect("/%s/login%s" % (app_base, url))


def get_request_remote_ip(rq):
	x_forwarded_for = rq.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		return x_forwarded_for.split(',')[-1].strip()
	else:
		return rq.META.get('REMOTE_ADDR')


def get_request_local_ip(rq):
	return socket.gethostbyname(rq.META.get('SERVER_NAME'))


def parse_metadata(md):
	try:
		meta = literal_eval(md)
		return {
			"agents": [User.objects.get(pk=a) for a in meta["agents"]]
		}
	except Exception:
		return {}


@register.filter
def item(dictionary, key):
	return dictionary.get(key)


@register.filter
def attr(obj, attr):
	return getattr(obj, attr)


@register.filter
def format_date(date, format):
	return date.strftime(format)


@register.filter
def equals(obj, obj2):
	return obj == obj2
