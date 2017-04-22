# SyZaCz web - plugin loading and initialization

import os
import glob
from django.conf.urls import url
from django.http import HttpResponse

from core.utils import validate_sessid

plugin_env = {
	"version": lambda: (0,0,1),
	"validate_sessid": validate_sessid
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
					lambda *args, **kwargs: buildView(globals()[p], u[1], *args, **kwargs)
				)
				for u in p_urls
			]
		)
	return urls

def buildView(plugin, callback, *args, **kwargs):
	print "building view for %s" % callback
	return HttpResponse(getattr(plugin, callback)(*args, **kwargs))