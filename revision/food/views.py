from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(req):
   return HttpResponse("hey hello user!")


def item(req):
   return HttpResponse("<h1>this is item view</h1>")