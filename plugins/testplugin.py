# SyZaCz web test plugin

env = {}

def init(plugin_env):
	global env
	env = plugin_env

def urls():
	return [
		[ "%s/test-plugin/%s", "test_plugin", None ]
	]


def test_plugin(rq, sessid):
	if env["validate_sessid"](sessid):
		return "Welcome from plugin view! sessid=%s" % sessid
	else:
		return "Core did not validate session!"