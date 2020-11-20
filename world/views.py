from django.shortcuts import render
from .models import Destinations
import json

# Create your views here.
def home_view(request):
    with open('world/json/world_countries.json', 'r') as file:
        data = json.load(file)
    context = {
        'countries': data['features']
    }
    return render(request, 'world/home.html', context)

def world_view(request):
    context = {
        'destinations': Destinations.objects.all()
    }
    print(context)
    return render(request, 'world/myworld.html', context)