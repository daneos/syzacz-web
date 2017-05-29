from django.contrib import admin
from core.models import *

admin.sites.AdminSite.site_header = "Database admin: SyZaCz-web"
admin.sites.AdminSite.site_title = "SyZaCz-web"

admin.site.register(User)
admin.site.register(Session)
admin.site.register(Log)
