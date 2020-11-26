from django.shortcuts import render, redirect
from .models import Destinations
import json
import folium
import pandas as pd
import sqlite3 as sql

# Create your views here.
def sign_in(request):
    return render(request, 'world/sign_in.html', {})


def sign_in(request):
    return render(request, 'world/sign_up.html', {})


def home_view(request):
    if request.method == 'POST':
        choice = request.POST
        been = False
        want_to_go = False
        if choice['status'] == 'Want to go!':
            want_to_go = True
        if choice['status'] == 'Already been!':
            been = True
        form = Destinations(country_name=choice['country_name'], been=been, want_to_go=want_to_go)
        form.save()
        return redirect('myworld')
    m = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)
    m.save('world/templates/world/map.html')
    # print(request.POST)
    with open('world/json/world_countries.json', 'r') as file:
        data = json.load(file)
    context = {
        'countries': data['features']
    }
    return render(request, 'world/home.html', context)


def world_view(request):
    connection = sql.connect('./db.sqlite3')
    destinations = pd.read_sql('select * from world_destinations', con=connection)

    my_map = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)

    # creates a map of all countries where want_to_go is true 
    folium.Choropleth(geo_data='world/json/world_countries.json',
                 name='My Countries',
                 data=destinations,
                 columns=['country_name', 'want_to_go'],
                 key_on='feature.properties.name',
                 fill_color='YlGn',
                 nan_fill_color='white'
                ).add_to(my_map)

    # creates a map of all countries where been is true 
    folium.Choropleth(geo_data='world/json/world_countries.json',
                 name='My Countries',
                 data=destinations,
                 columns=['country_name', 'been'],
                 key_on='feature.properties.name',
                 fill_color='YlGn',
                 nan_fill_color='white'
                ).add_to(my_map)

    my_map.save('world/templates/world/my_map.html')

    context = {
        'destinations': destinations
    }
    return render(request, 'world/myworld.html', context)