from django.core.exceptions import ObjectDoesNotExist
from models import Resource, Resource_using

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)

def urls():
	return [
		["%s/get_resource_information/(?P<resource_id>[0-9]+/$)", "get_resource_information", "get_resource_information.html"]
        ["%s/get_resource_information/$", "get_resource_information", "get_resource_information.html"]
        ["%s/get_resource_using_information/(?P<resource_id>[0-9]+)/$", "get_resource_using_information", "get_resource_using_information.html"]
        ["%s/get_resource__using_information/$", "get_resource_using_information", "get_resource_using_information.html"]
        ["%s/add_resource/$", "add_resource", "add_resource.html"]
        ["%s/add_resource_using/$", "add_resource_using", "add_resource_using.html"]
        ["%s/modify_resource_amount/(?P<resource_id>[0-9]+)/(?P<new_amount>[0-9]+)/$", "modify_resource_amount", "modify_resource_amount.html"]
    ]

def get_resource_information(rq, resource_id):

    if not(isinstance(resource_id, int )) or (resource_id < 0):
		return {"error":"Bad argument"}

	resource_model = env["getModel"]("Resource")

    try:
		resource = resource_model.objects.get(id=resource_id)
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}

    return {"result":resource}

def get_resource_information(rq):
	resource_model = env["getModel"]("Resource")
    try:
		resource = resource_model.objects.all()
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}

    return {"result": resource}


def get_resource_using_information(rq, resource_id):
	if not (isinstance(resource_id, int)) or (resource_id < 0):
		return {"error": "Bad argument"}

	resource_using_model = env["getModel"]("Resource_using")

	try:
		resource_using = resource_using_model.objects.get(resource_id=resource_id)
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"result": resource_using}


def get_tools_information(rq):
	resource_model = env["getModel"]("Resource")
    try:
	    resource = resource_model.objects.all()
    except ObjectDoesNotExist:
	    return {"error": "Object does not exist"}

    return {"result": resource}

def add_resource(rq):
    resource_name = rq.POST.get("resource_name")
    resource_description = rq.POST.get("resource_description")
    resource_remained = rq.POST.get("resource_remained")
    resource_remained_alarm = rq.POST.get("resource_remained_alarm")

    resource_model = env["getModel"]("Resource")

    try:
        resource_model.name = resource_name
        resource_model.description = resource_description
        resource_model.remained = resource_remained
        resource_model.remained_alarm = resource_remained_alarm
        resource_model.save()
    except Error:
        return {"error": "Cannot add new object"}

    return {"result": "0"}

def add_resource_using(rq):
    resource_use_date = rq.POST.get("resource_use_date")
    resource_amount = rq.POST.get("resource_amount")
    resource_comment = rq.POST.get("resource_comment")
    resource_member_id = rq.POST.get("resource_member_id")
    resource_id = rq.POST.get("resource_id")

    resource_model = env["getModel"]("Resource_using")

    try:
        resource_model.use_date = resource_use_date
        resource_model.amount = resource_amount
        resource_model.comment = resource_comment
        resource_model.member_id = resource_member_id
        resource_model.resource_id = resource_id
        resource_model.save()
    except Error:
        return {"error": "Cannot add new object"}
    return {"result": "0"}

def modify_resource_amount(rq, resource_id,new_ammount):
    resource_using_model = env["getModel"]("Resource_using")

    try:
        resource = resource_model.objects.get(resource_id=resource_id)
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}

    try:
        resource.ammount = new_ammount
        resource.save()
    except Error:
        return {"error": "Cannot add new object"}
    return {"result": "0"}
