from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.shortcuts import redirect

from conf import app_base
from core.version import Version
import hashlib

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,2)

def urls():
	return [
        ["%s/new_invoice$", "add_invoice", "invoice/add_invoice.template.html"],
        ["%s/add_invoice_file/(?P<id>[0-9]+)/$", "add_invoice_file", "invoice/add_invoice_file.template.html"], #templatka do wyslania pliku faktury uwaga redirect TODO
        ["%s/show_invoices$", "show_invoices", "invoice/history_invoice.template.html"],
        # podobna do powyzszej["%s/invoices/$", "invoices", None], #templatka do faktur transparency
        #["%s/show_invoice(?P<id>[a-z]+)/$", "show_invoice", "invoice/show_invoice.template.html"], #templatka do pokazania pojedynczej faktury
        #["%s/download_invoices$", "download_all", "invoice/download_invoices.template.html"] #templatka do pobrania wszystkich faktur
	]

def add_invoice(rq):
	context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}
	context.update(env["csrf"](rq))
	
	if rq.method == "POST":
		Session = env["getModel"]("Session")
		Invoice = env["getModel"]("Invoice")
		
		try:
			s = Session.objects.get(session_hash=env["sessid"](rq))
			hashed = hashlib
			
			invoice = Invoice()
			invoice.invoice_number = rq.POST.get("invoice_number")
			invoice.issue_date = rq.POST.get("issue_date")
			invoice.amount = rq.POST.get("amount")
			invoice.with_cashbacked = rq.POST.get("with_cashbacked")
			invoice.member_id = s.user
			invoice.permalink = ""
			invoice.save()
		except Error as e:
			return {"error": "Cannot add new object: %s" % e}
			
		return redirect("%s/add_invoice_file/%s/" % (app_base, invoice.id))
		
	return context
	

def show_invoices(rq):
	Invoice = env["getModel"]("Invoice")
	
	if rq.method == "GET":
		try:
			last_two_months = datetime.today() - timedelta(days=61)
			invoices = Invoice.objects.filter(issue_date__gte = last_two_months)
			context = {"invoices" : invoices}
			context.update(env["csrf"](rq))
		except ObjectDoesNotExist:
			return {"error:": "Object does not exist"}
		return context
	if rq.method == "POST":
		try:
			od = rq.POST.get("od")
			do = rq.POST.get("do")
			invoices = Invoice.objects.filter(issue_date__range=(start_date, end_date))
		except ObjectDoesNotExist:
			return {"error:": "Object does not exist"}
		return{"invoices": invoices}
	
def add_invoice_file(rq, id):
	Invoice = env["getModel"]("Invoice")
	context
	if rq.method == "GET":
		context.update(env["csrf"](rq))
	if rq.method == "POST":
		return ("text")
			
	return context