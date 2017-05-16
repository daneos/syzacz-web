from django.core.exceptions import ObjectDoesNotExist

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)

def urls():
	return [
		#[ "%s/addTool$", "addTool", "addTool.html" ]
		#["%s/showTools", "showTools", "addTool.html"]
		["%s/get_tool_information/123", "get_tool_information", "get_tool_information.html"]
        ["%s/get_tools_information/$", "get_tools_information", "get_tool_information.html"]
	]

def get_tool_information(rq, new_tool_info):

    if not(isinstance( new_tool_info, int )) or (newToolInfo < 0):
		return {"error":"Bad argument"}

    tool_model = env["getModel"]("Tool")

    try:
        tool = tool_model.objects.get(id=new_tool_info)
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}

    return {"result":tool}

def get_tools_information(rq):

    tool_model = env["getModel"]("Tool")

    try:
        tools = tool_model.objects.all()
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}

    return {"result": tools}

def add_tool(rq):










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
		"core_version": "%d.%d.%d" % ver
}