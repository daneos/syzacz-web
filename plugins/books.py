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
	return Version([0, 0, 2, "alpha"])


def urls():
	return [
		["%s/books.all$", "books_list", "books/books.template.html"],
		["%s/books.add$", "add_book", "books/add_book.template.html"],
		["%s/books.my$", "books_my", "books/books.template.html"],
		["%s/books.lent$", "books_lent", "books/lent_books.template.html"],
		["%s/books.return/(?P<book_id>[0-9]+)/$", "return_book", None],
		["%s/books.prolong/(?P<book_id>[0-9]+)/$", "prolong_book", "books/prolong_book.template.html"],
		["%s/book.lend/(?P<book_id>[0-9]+)/$", "lend_book", "books/lend_book.template.html"],
		["%s/book.show/(?P<book_id>[0-9]+)/$", "show_book", "books/show_book.template.html"]
	]


def books_list(rq):
	Book = env["getModel"]("Book")
	try:
		books = Book.objects.filter(available=True)
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}
	return {"books": books}


def books_my(rq):
	context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}

	Book = env["getModel"]("Book")
	Session = env["getModel"]("Session")
	Lent = env["getModel"]("Lent")
	session = Session.objects.get(session_hash=env["sessid"](rq))
	try:
		filtered_lents = {}
		books = Book.objects.filter(member_id=session.user)
		for book in books:
			lents = Lent.objects.filter(book=book)
			for lent in lents:
				if lent.return_date is None:
					filtered_lents[book] = lent
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	context.update({"books": books, "lents": filtered_lents, "display_edit": True})
	return context


def add_book(rq):
	if rq.method == "GET":
		Placement = env["getModel"]("Placement")
		context = {"placements": Placement.objects.all()}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		Session = env["getModel"]("Session")
		Book = env["getModel"]("Book")

		try:
			session = Session.objects.get(session_hash=env["sessid"](rq))

			book = Book()
			book.title = rq.POST.get("title")
			book.description = rq.POST.get("description")
			book.review = rq.POST.get("review")
			book.pages = rq.POST.get("pages")
			book.member_id = session.user
			placement = env["getModel"]("Placement").objects.get(pk=rq.POST.get("placement_id"))
			book.placement_id = placement
			book.save()
		except Error as e:
			return {"error": "Cannot add new object: %s" % e}

		return redirect("/%s/books.my?msg=Saved" % app_base)


def books_lent(rq):
	context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}

	Session = env["getModel"]("Session")
	Lent = env["getModel"]("Lent")
	session = Session.objects.get(session_hash=env["sessid"](rq))
	try:
		lents = {}
		for lent in Lent.objects.filter(member=session.user):
			if lent.return_date is None:
				lents[lent.book] = lent
		books = lents.keys()
	except ObjectDoesNotExist:
		return {"error": "Object does not exist"}

	context.update({"books": books, "lents": lents})
	return context


def show_book(rq, book_id):
	Book = env["getModel"]("Book")
	book = Book.objects.get(id=book_id)
	return {"book": book}


def lend_book(rq, book_id):
	Book = env["getModel"]("Book")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	if rq.method == "GET":
		book = Book.objects.get(pk=book_id)
		context = {"book": book}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		session = Session.objects.get(session_hash=env["sessid"](rq))
		book = Book.objects.get(pk=book_id)
		lent = Lent()
		lent.planned_return_date = rq.POST.get("return_date")
		lent.return_date = None
		lent.comment = ""
		lent.member = session.user
		lent.book = book
		lent.save()
		book.available = False
		book.save()
		return redirect("/%s/books.lent?msg=Saved" % app_base)


def return_book(rq, book_id):
	Book = env["getModel"]("Book")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	session = Session.objects.get(session_hash=env["sessid"](rq))

	book = Book.objects.get(pk=book_id)
	lent = Lent.objects.get(book=book, member=session.user, return_date=None)
	lent.return_date = datetime.now()
	lent.save()
	book.available = True
	book.save()

	return redirect("/%s/books.lent?msg=Saved" % app_base)


def prolong_book(rq, book_id):
	Book = env["getModel"]("Book")
	Lent = env["getModel"]("Lent")
	Session = env["getModel"]("Session")
	session = Session.objects.get(session_hash=env["sessid"](rq))
	book = Book.objects.get(pk=book_id)
	lent = Lent.objects.get(book=book, member=session.user, return_date=None)

	if rq.method == "GET":
		context = {"book": book, "lent": lent}
		context.update(env["csrf"](rq))
		return context

	if rq.method == "POST":
		lent.planned_return_date = rq.POST.get("return_date")
		lent.save()

		return redirect("/%s/books.lent?msg=Saved" % app_base)
