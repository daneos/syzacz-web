# SyZaCz web test plugin

from django.shortcuts import redirect
from conf import app_base

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return (0, 0, 2)


def urls():
	return [
		["%s/2-test-plugin", "test_plugin", "testplugin/test.template.html"],
		["%s/2-test-redirect", "test_redirect", None]
	]


def test_plugin(rq):
	ver = env["version"]()
	sessid = env["sessid"](rq)
	Session = env["getModel"]("Session")
	User = env["getModel"]("User")

	s = Session.objects.get(session_hash=sessid)
	u = User.objects.get(pk=s.user.id)

	return {
		"sessid": "2222222222222222",
		"user": "22222222",
		"core_version": "%d.%d.%d" % ver
	}


def test_redirect(rq):
	return redirect("/%s/home" % app_base)
