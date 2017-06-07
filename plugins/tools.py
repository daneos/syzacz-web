from django.core.exceptions import ObjectDoesNotExist
from django.db import Error

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)


def urls():
	return [
		["%s/tools.(?P<tool_id>[0-9]+)/$", "get_tool_information", "tools/.html"],
		["%s/tools.all$", "tools_list", "tools/tools.template.html"],
		["%s/tools.add_tool$", "add_tool", "tools/add_tool.template.html"]
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


def tools_list(rq):
	tool_model = env["getModel"]("Tool")
	try:
		tools = tool_model.objects.all()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"tools": tools}


def add_tool(rq):
	if rq.method == "GET":
		Placement = env["getModel"]("Placement")
		context = {"placements": Placement.objects.all()}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		name = rq.POST.get("name")
		description = rq.POST.get("description")
		# tool_is_able = rq.POST.get("tool_is_able")
		# tool_lent_permission = rq.POST.get("tool_lent_permission")
		tool_placement_id = rq.POST.get("placement_id") # zabezpieczyc czy istnieje takie miejsce

		Session = env["getModel"]("Session")
		Tool = env["getModel"]("Tool")

		try:
			s = Session.objects.get(session_hash=env["sessid"](rq))

			tool_model = Tool()
			tool_model.name = name
			tool_model.description = description
			# tool_model.is_able = tool_is_able
			# tool_model.lent_permission = tool_lent_permission
			tool_model.member_id = s.user
			placement = env["getModel"]("Placement").objects.get(pk=tool_placement_id)
			tool_model.placement_id = placement
			tool_model.save()
		except Error as e:
			return {"error": "Cannot add new object: %s" % e}

		return {"result": tool_model}
