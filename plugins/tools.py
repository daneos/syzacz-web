from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.shortcuts import redirect

from conf import app_base
from core.version import Version

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return Version([1, 0, 1, "beta"])


def urls():
	return [
		["%s/tools.all$", "tools_list", "tools/tools.template.html"],
		["%s/tools.my$", "tools_my", "tools/tools.template.html"],
		["%s/tools.lent$", "tools_lent", "tools/lent_tools.template.html"],
		["%s/tools.add$", "add_tool", "tools/add_tool.template.html"],
		["%s/tools.lend/(?P<id>[0-9]+)/$", "lend_tool", "tools/lend_tool.template.html"],
		["%s/tools.return/(?P<id>[0-9]+)/$", "return_tool", None],
		["%s/tools.prolong/(?P<id>[0-9]+)/$", "prolong_tool", "tools/prolong_tool.template.html"],
		["%s/tools.edit/(?P<id>[0-9]+)/$", "edit_tool", "tools/edit_tool.template.html"]
	]


def tools_list(rq):
	Tool = env["getModel"]("Tool")
	try:
		tools = Tool.objects.filter(available=True)
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"tools": tools}


def tools_my(rq):
	Tool = env["getModel"]("Tool")
	Session = env["getModel"]("Session")
	Lent = env["getModel"]("Lent")
	s = Session.objects.get(session_hash=env["sessid"](rq))
	try:
		filtered_lents = {}
		tools = Tool.objects.filter(member=s.user)
		for tool in tools:
			lents = Lent.objects.filter(tool=tool)
			for lent in lents:
				if lent.return_date is None:
					filtered_lents[tool] = lent
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"tools": tools, "lents": filtered_lents}


def tools_lent(rq):
	Session = env["getModel"]("Session")
	Lent = env["getModel"]("Lent")
	s = Session.objects.get(session_hash=env["sessid"](rq))
	try:
		lents = {}
		for lent in Lent.objects.filter(member=s.user):
			if lent.return_date is None:
				lents[lent.tool] = lent
		tools = lents.keys()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"tools": tools, "lents": lents}


def add_tool(rq):
	if rq.method == "GET":
		Placement = env["getModel"]("Placement")
		context = {"placements": Placement.objects.all()}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		Session = env["getModel"]("Session")
		Tool = env["getModel"]("Tool")

		try:
			s = Session.objects.get(session_hash=env["sessid"](rq))

			tool = Tool()
			tool.name = rq.POST.get("name")
			tool.description = rq.POST.get("description")
			tool.lend_permission = bool(rq.POST.get("permission"))
			tool.member = s.user
			placement = env["getModel"]("Placement").objects.get(pk=rq.POST.get("placement_id"))
			tool.placement = placement
			tool.save()
		except Error as e:
			return {"error": "Cannot add new object: %s" % e}

		return redirect("/%s/tools.my" % app_base)


def lend_tool(rq, id):
	Tool = env["getModel"]("Tool")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	if rq.method == "GET":
		tool = Tool.objects.get(pk=id)
		context = {"tool": tool}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		s = Session.objects.get(session_hash=env["sessid"](rq))
		tool = Tool.objects.get(pk=id)
		lent = Lent()
		lent.planned_return_date = rq.POST.get("return_date")
		lent.return_date = None
		lent.comment = ""
		lent.member = s.user
		lent.tool = tool
		lent.save()
		tool.available = False
		tool.save()
		return redirect("/%s/tools.lent" % app_base)


def return_tool(rq, id):
	Tool = env["getModel"]("Tool")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	s = Session.objects.get(session_hash=env["sessid"](rq))

	tool = Tool.objects.get(pk=id)
	lent = Lent.objects.get(tool=tool, member=s.user, return_date=None)
	lent.return_date = datetime.now()
	lent.save()
	tool.available = True
	tool.save()

	return redirect("/%s/tools.lent" % app_base)


def prolong_tool(rq, id):
	Tool = env["getModel"]("Tool")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	s = Session.objects.get(session_hash=env["sessid"](rq))
	tool = Tool.objects.get(pk=id)
	lent = Lent.objects.get(tool=tool, member=s.user, return_date=None)

	if rq.method == "GET":
		context = {"tool": tool, "lent": lent}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		lent.planned_return_date = rq.POST.get("return_date")
		lent.save()

		return redirect("/%s/tools.lent" % app_base)


def edit_tool(rq, id):
	Tool = env["getModel"]("Tool")
	Lent = env["getModel"]("Lent")
	Placement = env["getModel"]("Placement")

	tool = Tool.objects.get(pk=id)
	lents = Lent.objects.filter(tool=tool)
	placements = Placement.objects.all()

	if rq.method == "GET":
		context = {"tool": tool, "lents": lents, "placements": placements}
		context.update(env["csrf"](rq))
		return context
