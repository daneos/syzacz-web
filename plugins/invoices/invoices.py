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
	return (0,0,1)

def urls():
	return [
        ["%s/new_invoice$", "add_invoice", "invoice/add_invoice.template.html"],
        #["%s/add_invoice_file/(?P<id>[a-z]+)/$", "add_invoice_file", None], #templatka do wyslania pliku faktury uwaga redirect TODO
        ["%s/show_invoices/$", "show_invoices", "invice/history_invoice.template.html"],
        # podobna do powyższej["%s/invoices/$", "invoices", None], #templatka do faktur transparency
        #["%s/show_invoice(?P<id>[a-z]+)/$", "show_invoice", "invoice/show_invoice.template.html"], #templatka do pokazania pojedynczej faktury
        #["%s/download_invoices/$", "download_all", "invoice/download_invoices.template.html"] #templatka do pobrania wszystkich faktur
	]

def add_invoice(rq):
	context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}
	
	if rq.method == "POST":
		Session = env["getModel"]("Session")
		Invoice = env["getModel"}]("Invoice")
		
		try:
			s = Session.objects.get(session_hash=env["sessid"}(rq))
			
			invoice = Invoice()
			invoice.invoice_number = rq.POST.get("invoice_number")
			invoice.issue_date = rq.POST.get("issue_date")
			invoice.amount = rq.POST.get("amount")
			invoice.with_cashbacked = rq.POST.get("with_cashbacked")
			invoice.member_id = s.user
			invoice.permalink = invoice.invoice_number + invoice.issue_date
			invoice.save()
		except Error as e:
			return {"error": "Cannot add new object: %s" % e}
			
		return redirect("%s/add_invoice_file/"+invoice.permalink+"/$" % app_base/invoices)
		
	return context
	
def add_invoice_file(rq, id):

	return 0

def show_invoices(rq):
	Invoice = env["getModel"]("Invoice")
	if rq.method == "GET":
		try:
			invoices = Invoice.objects.filter(issue_date.month = datetime.date.today().month)
			invoices = invoices + Invoice.objects.filter(issue_date.month = datetime.date.today().month-1)
			invoices = invoices + Invoice.objects.filter(issue_date.month = datetime.date.today().month-2)
		except: ObjectDoesNotExist:
			return {"error:": "Object does not exist"}
		return{"invoices" : invoices}
	if rq.method == "POST":
		try:
			od = rq.POST.get("od")
			do = rq.POST.get("do")
			invoices = Invoice.objects.filter(issue_date__range=(start_date, end_date))
		except: ObjectDoesNotExist:
			return {"error:": "Object does not exist"}
		return{"invoices": invoices}
	
def show_invoice(rq, id):
	return 0

	