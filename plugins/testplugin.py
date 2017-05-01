# SyZaCz web test plugin

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,2)

def urls():
	return [
		[ "%s/test-plugin/%s", "test_plugin", "testplugin/test.template.html" ]
	]


def test_plugin(rq, sessid):
	if env["validate_sessid"](sessid):
		ver = env["version"]()
		return {
			"sessid": sessid,
			"core_version": "%d.%d.%d" % ver
		}
	else:
		return { "error":"Core did not validate session!" }