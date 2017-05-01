# SyZaCz web test plugin

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,2)

def urls():
	return [
		[ "%s/test-plugin", "test_plugin", "testplugin/test.template.html" ]
	]


def test_plugin(rq):
	if env["validate_sessid"](rq):
		ver = env["version"]()
		return {
			"sessid": env["sessid"](rq),
			"core_version": "%d.%d.%d" % ver
		}
	else:
		return { "error":"Core did not validate session!" }