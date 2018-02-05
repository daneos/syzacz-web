from django.contrib import admin
from core.models import *

admin.sites.AdminSite.site_header = "Database admin: SyZaCz-web"
admin.sites.AdminSite.site_title = "SyZaCz-web"

admin.site.register(User)
admin.site.register(Session)
admin.site.register(Log)
admin.site.register(Tool)
admin.site.register(Book)
admin.site.register(Placement)
admin.site.register(Lent)
admin.site.register(Resource)
admin.site.register(ResourceUsage)
admin.site.register(Invoice)
admin.site.register(Rfid)
admin.site.register(Training)
admin.site.register(Special_function)
admin.site.register(Members_special_function)
