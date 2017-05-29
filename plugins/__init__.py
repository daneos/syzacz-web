# SyZaCz web - plugin loading and initialization

import os
import glob
from django.conf.urls import url
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.template.context_processors import csrf

from conf import app_base
from core.utils import *
from core.log import log

plugin_env = {
	"version": lambda: (0, 0, 2),
	"get_object_or_404": get_object_or_404,
	"sessid": sessid,
	"log": log,
	"getModel": lambda name: apps.get_model(app_label="core", model_name=name),
	"csrf": csrf
}

plugin_list = []
for f in glob.glob(os.path.dirname(__file__) + "/*"):
	if os.path.isfile(f) and not os.path.basename(f).startswith('_') and not os.path.basename(f).endswith("pyc"):
		plugin_list.append(os.path.basename(f)[:-3])

print plugin_list

for p in plugin_list:
	try:
		__import__(p, locals(), globals())
		ver = globals()[p].init(plugin_env)
		log("[LOAD] %s %d.%d.%d" % ((p,) + ver))
	except Exception as e:
		log("[LOAD] Error loading plugin %s: %s" % (p, str(e)))


def makeUrls(base_url):
	urls = []
	for p in plugin_list:
		p_urls = globals()[p].urls()
		urls.extend(
			[
				url(
					r"%s" % (u[0] % base_url),
					buildView(p, u)
				)
				for u in p_urls
			]
		)
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
			return syzacz_render(template, context)
		else:
			return HttpResponse(context)
	else:
		return session_expired("/%s" % url)
