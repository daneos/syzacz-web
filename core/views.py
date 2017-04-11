from django.shortcuts import render
from django.http import HttpResponse

def test_core(rq):
	return HttpResponse("Welcome from core view!")
