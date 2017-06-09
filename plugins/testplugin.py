# SyZaCz web test plugin

from django.shortcuts import redirect
from conf import app_base
from core.version import Version

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return Version([0, 0, 4, "stable"])


def urls():
	return [
		["%s/test-plugin", "test_plugin", "testplugin/test.template.html"],
		["%s/test-redirect", "test_redirect", None]
	]


def test_plugin(rq):
	ver = env["version"]()
	sessid = env["sessid"](rq)
	Session = env["getModel"]("Session")
	User = env["getModel"]("User")

	s = Session.objects.get(session_hash=sessid)
	u = User.objects.get(pk=s.user.id)

	return {
		"sessid": sessid,
		"user": u.cn,
		"core_version": str(ver)
	}


def test_redirect(rq):
	return redirect("/%s/home" % app_base)
