"""core_sv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import conf
import core
import plugins


base_url = r"^%s" % conf.app_base
session = r"(?P<sessid>[0-9a-f\-]+)"

urlpatterns = [
	url(r'%s/dba/' % base_url,							include(admin.site.urls)),

	url(r'%s/test-core$' % base_url, 					'core.views.test_core'),

	url(r'%s/login$' % base_url,						'core.views.login'),
	url(r'%s/logout/%s$' % (base_url, session),			'core.views.logout'),
	url(r'%s/home/%s$' % (base_url, session),			'core.views.home')
]

urlpatterns.extend(plugins.makeUrls(base_url, session))