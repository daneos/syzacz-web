from django.core.exceptions import ObjectDoesNotExist

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)

def urls():
	return [
		["%s/get_book_information/(?P<book_id>[0-9]+)/$", "get_book_information", None],#"get_book_information.html"],
		["%s/get_books_information/$", "get_books_information", None],#"get_book_information.html"],
		["%s/add_book/(?P<member_id>[0-9]+)/(?P<placement_id>[0-9]+)/$", "add_book", "add_book.html"]
	]

def get_book_information(rq, book_id):

	if book_id < 0:
		return {"error":"Bad argument"}

	book_model = env["getModel"]("book")

	try:
		book = book_model.objects.get(id=book_id)
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"result":book}

def get_books_information(rq):
	book_model = env["getModel"]("book")
	try:
		books = book_model.objects.all()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	return {"result": books}

def add_book(rq, member_id, placement_id):
	book_description = rq.POST.get("book_description")
	book_is_able = rq.POST.get("book_is_able")
	book_lent_permission = rq.POST.get("book_lent_permission")
	book_member_id = member_id #zabezpeiczyc czy istnieje taki member
	book_placement_id = placement_id # zabezpieczyc czy istnieje takie miejsce

	book_model = env["getModel"]("book")

	try:
		book_model.description = book_description
		book_model.is_able = book_is_able
		book_model.lent_permission = book_lent_permission
		book_model.member_id = book_member_id
		book_model.placement_id = book_placement_id
		book_model.save()
	except Error:
		return {"error": "Cannot add new object"}

	return {"result": "0"}
