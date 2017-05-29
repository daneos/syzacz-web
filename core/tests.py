from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from models import *


class LandingPageTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_landing_page(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 302)
		self.assertTrue(reverse("core.views.login") in str(response))


class AuthSystemTest(TestCase):
	def setUp(self):
		self.client = Client()
		User.objects.create(ldap="cn=test", cn="test", name="Test", surname="Testowy", email="test@example.com", password="test")

	def test_login_page(self):
		response = self.client.get(reverse("core.views.login"))
		self.assertEqual(response.status_code, 200)

	def test_good_credentials_and_logout(self):
		response = self.client.post(reverse("core.views.login"), {"username": "test", "password": "test"})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(reverse("core.views.home") in str(response))
		self.assertTrue("Set-Cookie: syzacz_sessid" in str(response.cookies))

		sessid = str(response.cookies).split("=")[1].split(";")[0]

		s = Session.objects.get(session_hash=sessid)
		self.assertTrue(s.active)

		response = self.client.get(reverse("core.views.logout"), COOKIE="syzacz_sessid=%s" % sessid)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(reverse("core.views.login") in str(response))

		s = Session.objects.get(session_hash=sessid)
		self.assertFalse(s.active)

	def test_bad_cn(self):
		response = self.client.post(reverse("core.views.login"), {"username": "nonexistent", "password": "test"})
		self.assertEqual(response.status_code, 200)
		self.assertTrue("Invalid user name or password" in str(response))

	def test_bad_password(self):
		response = self.client.post(reverse("core.views.login"), {"username": "test", "password": "wrongpassword"})
		self.assertEqual(response.status_code, 200)
		self.assertTrue("Invalid user name or password" in str(response))

	def test_next_url(self):
		next_url="/some/random/url"
		response = self.client.post("%s?next=%s" % (reverse("core.views.login"), next_url), {"username": "test", "password": "test"})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(next_url in str(response))
		self.assertTrue("Set-Cookie: syzacz_sessid" in str(response.cookies))
