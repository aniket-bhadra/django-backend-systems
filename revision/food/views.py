from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.
def index(req):
   item_list = Item.objects.all()
   context={
      "item_list":item_list
   }
   return render(req,"food/index.html",context)

def detail(req,item_id):
   item= Item.objects.get(pk=item_id)
   context={
      "item":item
   }
   return render(req,"food/details.html",context)
def item(req):
   return HttpResponse("hey hey this is item")