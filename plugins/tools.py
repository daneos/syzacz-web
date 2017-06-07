from django.core.exceptions import ObjectDoesNotExist

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)


def urls():
	return [
		["%s/tool/(?P<tool_id>[0-9]+)/$", "get_tool_information", "tools/.html"],
		["%s/tools/$", "get_tools_information", "tools/tools.template.html"],
		["%s/add_tool/$", "add_tool", "tools/add_tool.template.html"]
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


def add_tool(rq):
	if rq.method == "GET":
		context = {}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		tool_description = rq.POST.get("tool_description")
		tool_is_able = rq.POST.get("tool_is_able")
		tool_lent_permission = rq.POST.get("tool_lent_permission")
		tool_placement_id = rq.POST.get("placement_id") # zabezpieczyc czy istnieje takie miejsce

		Session = env["getModel"]("Session")
		tool_model = env["getModel"]("Tool")

		try:
			s = Session.objects.get(session_hash=env["sessid"](rq))

			tool_model.description = tool_description
			tool_model.is_able = tool_is_able
			tool_model.lent_permission = tool_lent_permission
			tool_model.member_id = s.user
			placement = env["getModel"]("Placement").objects.get(pk=tool_placement_id)
			tool_model.placement_id = placement
			tool_model.save()
		except Error:
			return {"error": "Cannot add new object"}

		return {"result": "0"}
