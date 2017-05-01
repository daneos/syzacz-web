# SyZaCz web - plugin loading and initialization

import os
import glob
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from core.utils import *
from core.log import log

plugin_env = {
	"version": lambda: (0,0,1),
	"validate_sessid": validate_sessid,
	"get_object_or_404": get_object_or_404,
	"log": log
}

plugin_list = []
for f in glob.glob(os.path.dirname(__file__)+"/*"):
	if os.path.isfile(f) and not os.path.basename(f).startswith('_') and not os.path.basename(f).endswith("pyc"):
		plugin_list.append(os.path.basename(f)[:-3])

print plugin_list

for p in plugin_list:
	try:
		__import__(p, locals(), globals())
		ver = globals()[p].init(plugin_env)
		print "Loaded plugin: %s %d.%d.%d" % ((p,) + ver)
	except Exception as e:
		print "Error loading plugin %s: %s" % (p, str(e))

def makeUrls(base_url, session):
	urls = []
	for p in plugin_list:
		p_urls = globals()[p].urls()
		urls.extend(
			[
				url(
					r"%s" % (u[0] % (base_url, session)),
					lambda *args, **kwargs: buildView(globals()[p], u[1], u[2], *args, **kwargs)
				)
				for u in p_urls
			]
		)
	return urls

def buildView(plugin, callback, template, *args, **kwargs):
	print "building view for %s" % callback
	if template:
		return syzacz_render(template, getattr(plugin, callback)(*args, **kwargs))
	else:
		return HttpResponse(getattr(plugin, callback)(*args, **kwargs))