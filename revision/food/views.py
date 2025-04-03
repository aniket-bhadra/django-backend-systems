from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.
def index(req):
   Item_list = Item.objects.all()
   return HttpResponse(Item_list)


def item(req):
   return HttpResponse("<h1>this is item view</h1>")