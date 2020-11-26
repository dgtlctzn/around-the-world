from django.shortcuts import render, redirect, get_object_or_404
from .models import Destinations, User
from .forms import SignIn, SignUp
import json
import folium
import pandas as pd
import sqlite3 as sql

# Create your views here.
def sign_in_view(request):
    sign_in = SignIn()
    if request.method == 'POST':
        sign_in = SignIn(request.POST)
        if sign_in.is_valid():
            print(sign_in.cleaned_data)
    context = {
        'sign_in_form': sign_in
    }
    return render(request, 'world/sign_in.html', context)


def sign_up_view(request):
    sign_up = SignUp(request.POST or None)
    if sign_up.is_valid():
        sign_up.save()
        sign_up = SignUp()
        return redirect('home')
    else:
        print(sign_up.errors)
    context = {
        'sign_up_form': sign_up
    }
    return render(request, 'world/sign_up.html', context)


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


def world_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    connection = sql.connect('./db.sqlite3')
    destinations = pd.read_sql(f'select * from world_destinations where user_id_id = {user.id}', con=connection)
    
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