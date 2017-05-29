from django.core.exceptions import ObjectDoesNotExist

env = {}

def init(plugin_env):
	global env
	env = plugin_env
	return (0,0,1)

def urls():
	return [
        ["%s/new_invoice/", "add_info_about_new_invoice", None], #templatka do wypelnienia informacji o nowej fakturze
        ["%s/add_invoice_file/", "add_file", None], #templatka do wyslania pliku faktury
        ["%s/show_invoices/", "check_invoices", None], #templatka do wyswietlenia wszystkich faktur i ich przegladania
        ["%s/invoices/", "invoices", None], #templatka do faktur transparency
        ["%s/show_invoice/", "show_invoice", None], #templatka do pokazania pojedynczej faktury
        ["%s/download_invoices", "download_all", None] #templatka do wszystkich faktur
	]
