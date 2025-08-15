from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MovieSerializer
from .models import MovieData

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
   queryset = MovieData.objects.all()
   serializer_class= MovieSerializer

class ActionView(viewsets.ModelViewSet):
   queryset= MovieData.objects.filter(typ="fiction")
   serializer_class= MovieSerializer