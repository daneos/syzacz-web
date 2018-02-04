# SyZaCz web - plugin loading and initialization

import os
import glob
from django.conf.urls import url
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.template.context_processors import csrf

from conf import app_base, version, plugin_blacklist
from core.utils import *
from core.log import log

plugin_env = {
	"version": lambda: version,
	"get_object_or_404": get_object_or_404,
	"sessid": sessid,
	"log": log,
	"getModel": lambda name: apps.get_model(app_label="core", model_name=name),
	"csrf": csrf,
	"parse_metadata": parse_metadata
}

plugin_list = []
for f in glob.glob(os.path.dirname(__file__) + "/*"):
	fn = os.path.basename(f)
	if os.path.isfile(f) and not fn.startswith('_') and not fn.endswith("pyc"):
		module_name = fn[:-3]
		if module_name in plugin_blacklist:
			log("[LOAD] Not loading %s; blacklisted" % module_name)
			continue
		plugin_list.append(module_name)

for p in plugin_list:
	try:
		__import__(p, locals(), globals())
		ver = globals()[p].init(plugin_env)
		log("[LOAD] %s %s" % (p, str(ver)))
	except Exception as e:
		log("[LOAD] Error loading plugin %s: %s" % (p, str(e)))


def makeUrls(base_url):
	urls = []
	for p in plugin_list:
		p_urls = globals()[p].urls()
		# urls.extend(
		# 	[
		# 		url(
		# 			r"%s" % (u[0] % base_url),
		# 			lambda *args, **kwargs: buildView(globals()[p], u[0] % app_base, u[1], u[2], *args, **kwargs)
		# 		)
		# 		for u in p_urls
		# 	]
		# )
		for u in p_urls:
			uc = url(
					r"%s" % (u[0] % base_url),
					buildView(p, u)
				)
			urls.append(uc)
	return urls


def buildView(plugin, urlconf):
	log("[BUILD-VIEW] %s.%s" % (plugin, urlconf))
	return lambda *args, **kwargs: pluginCallback(globals()[plugin], urlconf[0] % app_base, urlconf[1], urlconf[2], *args, **kwargs)


def pluginCallback(plugin, url, callback, template, *args, **kwargs):
	log("[RUN] %s.%s" % (plugin.__name__, callback))
	if validate_sessid(args[0]):
		context = getattr(plugin, callback)(*args, **kwargs)
		if type(context) == HttpResponseRedirect:
			return context
		if template:
			s = Session.objects.get(session_hash=sessid(args[0]))
			context.update({"user": s.user, "plugin_blacklist": plugin_blacklist})
			# print context
			return syzacz_render(template, context)
		else:
			return HttpResponse(context)
	else:
		rq = args[0]
		next_url = rq.path
		return session_expired("%s" % next_url)
