import json
from datetime import datetime
from time import time
from uuid import uuid4

from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def response(status, data):
	body = {"status": status}
	body["data"] = data
	body["timestamp"] = int(time())
	body["uuid"] = str(uuid4())
	return HttpResponse(json.dumps(body, indent=1), content_type="application/json")

def validate_sessid(sessid):
	# session = get_object_or_404(Session, session_hash=sessid)
	# if session.active:
	# 	session.last_activity = datetime.now()
	# 	session.save()
	# return session.active
	print "requested validation of session ID=%s" % sessid
	return True

def session_expired():
	return response("error", "9001 Session expired.")