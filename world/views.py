from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.db import connection
from .models import Destinations, User
from .forms import SignIn, SignUp
import json
import folium
import pandas as pd
from datetime import datetime

# Create your views here.
def sign_in_view(request):
    sign_in = SignIn()
    if request.method == 'POST':
        sign_in = SignIn(request.POST)
        if sign_in.is_valid():
            try:
                login = sign_in.cleaned_data
                user = User.objects.get(username=login['username'], password=login['password'])
                return redirect(f'myworld/{user.id}')
            except User.DoesNotExist as err:
                sign_in.add_error('username', 'Incorrect username and password combination.')
    context = {
        'sign_in_form': sign_in
    }
    return render(request, 'world/sign_in.html', context)


def sign_up_view(request):
    sign_up = SignUp(request.POST or None)
    if sign_up.is_valid():
        sign_up.save()
        new_user = User.objects.get(username=sign_up.clean()['username'])
        sign_up = SignUp()
        return redirect(f'home/{new_user.id}/')
    else:
        print(sign_up.errors)
    context = {
        'sign_up_form': sign_up
    }
    return render(request, 'world/sign_up.html', context)


def home_view(request, user_id):
    if request.method == 'POST':
        choice = request.POST
        been = False
        want_to_go = False
        if choice['status'] == 'Want to go!':
            want_to_go = True
        if choice['status'] == 'Already been!':
            been = True
        user = User.objects.get(id=user_id)
        form = Destinations(country_name=choice['country_name'], been=been, want_to_go=want_to_go, user_id=user)
        form.save()
        return redirect(f'/myworld/{user_id}')

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
    my_countries = Destinations.objects.filter(user_id=user_id)
    # formats django db query for pandas
    country_dict = {}
    for n, country in enumerate(my_countries):
        country_dict[n] = {'name': country.country_name, 'been': country.been, 'want_to_go': country.want_to_go}
    destinations = pd.DataFrame.from_dict(country_dict, orient='index')

    my_map = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)

    # creates a map of all countries where want_to_go is true 
    layer_one = folium.Choropleth(geo_data='world/json/world_countries.json',
                 name='My Countries',
                 data=destinations,
                 columns=['name', 'want_to_go'],
                 key_on='feature.properties.name',
                 fill_color='YlGn',
                 nan_fill_color='white'
                )

    # creates a map of all countries where been is true 
    layer_two = folium.Choropleth(geo_data='world/json/world_countries.json',
                 name='My Countries',
                 data=destinations,
                 columns=['name', 'been'],
                 key_on='feature.properties.name',
                 fill_color='YlGn',
                 nan_fill_color='white'
                )

    remove_legend(layer_one, my_map)
    remove_legend(layer_two, my_map)

    dt = datetime.now()
    my_map.save(f'world/templates/world/my_map{dt}.html')
    file = f'world/my_map{dt}.html'

    context = {
        'destinations': my_countries,
        'user_id': user_id,
        'no_background': True,
        'user': User.objects.get(id=user_id),
        'file': file
    }
    return render(request, 'world/myworld.html', context)