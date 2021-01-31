from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db import connection
from .models import Destinations
from .forms import SignIn, SignUp
import json
import folium
import pandas as pd
from datetime import datetime
from django.contrib.auth.models import User
from django.core.cache import cache

# Create your views here.
def sign_in_view(request):
    sign_in = SignIn()
    if request.method == 'POST':
        sign_in = SignIn(request.POST)
        if sign_in.is_valid():
            user_login = sign_in.cleaned_data
            user = authenticate(username=user_login['username'], password=user_login['password'])
            login(request, user)
            return redirect(f'myworld/{user.id}')
    context = {
        'sign_in_form': sign_in
    }
    return render(request, 'world/sign_in.html', context)


def sign_up_view(request):
    sign_up = SignUp(request.POST or None)
    if sign_up.is_valid():
        user = sign_up.save(commit=False)
        password = sign_up.cleaned_data['password']
        user.set_password(password)
        user.save()
        new_user = authenticate(request, username=user.username, password=password)
        login(request, new_user)
        sign_up = SignUp()
        return redirect(f'home/{new_user.id}/')
    else:
        print(sign_up.errors)
    context = {
        'sign_up_form': sign_up
    }
    return render(request, 'world/sign_up.html', context)


def home_view(request, user_id):
    user = request.user
    if not user.is_authenticated or int(user_id) != user.id:
        return redirect('/')
    if request.method == 'POST':
        print(request.POST)
        if 'country_name' in request.POST:
            choice = request.POST
            been = False
            want_to_go = False
            if choice['status'] == 'Want to go!':
                want_to_go = True
            if choice['status'] == 'Already been!':
                been = True
            User = get_user_model()
            user = User.objects.get(id=user_id)
            form = Destinations(country_name=choice['country_name'], been=been, want_to_go=want_to_go, user_id=user)
            form.save()
            return redirect(f'/myworld/{user_id}')
        elif 'logout' in request.POST:
            logout(request)
            return redirect('/')

    m = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)
    m.save('world/templates/world/map.html')

    with open('world/json/world_countries.json', 'r') as file:
        data = json.load(file)
    context = {
        'countries': data['features'],
        'user_id': user_id
    }
    return render(request, 'world/home.html', context)


# removes the legend on the choropleth map and adds layer to map
def remove_legend(layer, mymap):
    for key in layer._children:
        if key.startswith('color_map'):
            del(layer._children[key])
    layer.add_to(mymap)


def world_view(request, user_id):
    user = request.user
    if not user.is_authenticated or int(user_id) != user.id:
        return redirect('/')
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    # postgres db query to pandas
    destinations = pd.read_sql(f'select * from world_destinations where user_id_id = {user_id}', con=connection)

    my_map = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)

    # creates a map of all countries where want_to_go is true 
    layer_one = folium.Choropleth(geo_data='world/json/world_countries.json',
                name='My Countries',
                data=destinations,
                columns=['country_name', 'want_to_go'],
                key_on='feature.properties.name',
                fill_color='YlGn',
                nan_fill_color='white'
                )

    # creates a map of all countries where been is true 
    layer_two = folium.Choropleth(geo_data='world/json/world_countries.json',
                name='My Countries',
                data=destinations,
                columns=['country_name', 'been'],
                key_on='feature.properties.name',
                fill_color='YlGn',
                nan_fill_color='white'
                )

    remove_legend(layer_one, my_map)
    remove_legend(layer_two, my_map)

    # gives html file a unique file name
    dt = datetime.now()
    my_map.save(f'world/templates/world/my_map{dt}.html')
    file = f'world/my_map{dt}.html'

    context = {
        'destinations': destinations.to_dict(orient='index').values(),
        'user_id': user_id,
        'no_background': True,
        'user': User.objects.get(id=user_id),
        'file': file
    }
    return render(request, 'world/myworld.html', context)
