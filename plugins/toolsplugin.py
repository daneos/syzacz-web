from django.core.exceptions import ObjectDoesNotExist

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)

def urls():
	return [
		["%s/get_tool_information/(?P<tool_id>[0-9]+)/$", "get_tool_information", None],#"get_tool_information.html"],
		["%s/get_tools_information/$", "get_tools_information", None],#"get_tool_information.html"],
		["%s/add_tool/(?P<member_id>[0-9]+)/(?P<placement_id>[0-9]+)/$", "add_tool", "add_tool.html"]
	]

def get_tool_information(rq, tool_id):

	if tool_id < 0:
		return {"error":"Bad argument"}

	tool_model = env["getModel"]("Tool")

	try:
		tool = tool_model.objects.get(id=tool_id)
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

def add_tool(rq, member_id, placement_id):
	tool_description = rq.POST.get("tool_description")
	tool_is_able = rq.POST.get("tool_is_able")
	tool_lent_permission = rq.POST.get("tool_lent_permission")
	tool_member_id = member_id #zabezpeiczyc czy istnieje taki member
	tool_placement_id = placement_id # zabezpieczyc czy istnieje takie miejsce

	tool_model = env["getModel"]("Tool")

	try:
		tool_model.description = tool_description
		tool_model.is_able = tool_is_able
		tool_model.lent_permission = tool_lent_permission
		tool_model.member_id = tool_member_id
		tool_model.placement_id = tool_placement_id
		tool_model.save()
	except Error:
		return {"error": "Cannot add new object"}

	return {"result": "0"}
