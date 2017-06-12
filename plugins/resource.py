from django.shortcuts import redirect

from conf import app_base
from core.version import Version
from core.models import Resource, ResourceUsage, Session
from core.utils import sessid

env = {}


def init(plugin_env):
	global env
	env = plugin_env
	return Version([0, 0, 2, "alpha"])


def urls():
	return [
		["%s/resource.all$", "resource_list", "resource/resources.template.html"],
		["%s/resource/(?P<id>[0-9]+)/$", "resource_info", "resource/resource.template.html"],
		["%s/resource.add$", "add_resource", "resource/add_resource.template.html"],
		["%s/resource.use/(?P<id>[0-9]+)/$", "use_resource", "resource/use_refill_resource.template.html"],
		["%s/resource.refill/(?P<id>[0-9]+)/$", "refill_resource", "resource/use_refill_resource.template.html"],
		["%s/resource.edit/(?P<id>[0-9]+)/$", "edit_resource", "resource/edit_resource.template.html"],
		["%s/resource.alarm$", "resource_alarm", "resource/resources.template.html"]
	]


def resource_list(rq):
	context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}
	resources = Resource.objects.all()
	context.update({"resources": resources})
	return context


def resource_info(rq, id):
	res = Resource.objects.get(pk=id)
	usage = ResourceUsage.objects.filter(resource=res)
	return {"resource": res, "usage": usage}


def add_resource(rq):
	if rq.method == "GET":
		context = {}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		try:
			res = Resource()
			res.name = rq.POST.get("name")
			res.description = rq.POST.get("description")
			res.amount = rq.POST.get("amount")
			res.alarm = rq.POST.get("alarm")
			res.save()
		except Exception as e:
			redirect("/%s/resource.all?error=%s" % (app_base, str(e)))
		return redirect("/%s/resource.all?msg=Saved" % app_base)


def use_resource(rq, id):
	res = Resource.objects.get(pk=id)

	if rq.method == "GET":
		context = {"resource": res, "use_refill": "use"}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		s = Session.objects.get(session_hash=sessid(rq))
		amount = rq.POST.get("amount")
		try:
			usage = ResourceUsage()
			usage.amount = amount
			usage.resource = res
			usage.member = s.user
			usage.comment = rq.POST.get("comment")
			res.use(int(amount))
			res.save()
			usage.save()
		except Exception as e:
			return redirect("/%s/resource.all?error=%s" % (app_base, str(e)))
		return redirect("/%s/resource.all?msg=Saved" % app_base)


def refill_resource(rq, id):
	res = Resource.objects.get(pk=id)

	if rq.method == "GET":
		context = {"resource": res, "use_refill": "refill"}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		amount = rq.POST.get("amount")
		try:
			res.refill(int(amount))
			res.save()
		except Exception as e:
			return redirect("/%s/resource.all?error=%s" % (app_base, str(e)))
		return redirect("/%s/resource.all?msg=Saved" % app_base)


def edit_resource(rq, id):
	res = Resource.objects.get(pk=id)

	if rq.method == "GET":
		context = {"resource": res}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		try:
			res.name = rq.POST.get("name")
			res.description = rq.POST.get("description")
			res.alarm = rq.POST.get("alarm")
			res.save()
		except Exception as e:
			return redirect("/%s/resource.all?error=%s" % (app_base, str(e)))
		return redirect("/%s/resource.all?msg=Saved" % app_base)


def resource_alarm(rq):
	context = {}
	resources = [r for r in Resource.objects.all() if r.is_alarm()]
	context.update({"resources": resources})
	return context
