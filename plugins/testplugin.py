# SyZaCz web test plugin

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,2)

def urls():
	return [
		[ "%s/test-plugin/%s", "test_plugin", None ]
	]


def test_plugin(rq, sessid):
	if env["validate_sessid"](sessid):
		ver = env["version"]()
		return "Welcome from plugin view! sessid=%s<br>Core version: %d.%d.%d" % ((sessid,)+ver)
	else:
		return "Core did not validate session!"