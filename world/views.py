from django.shortcuts import render
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
    return render(request, 'world/myworld.html', {})