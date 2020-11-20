from django.shortcuts import render, redirect
from .models import Destinations
import json
import folium
import pandas as pd

# Create your views here.
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
    my_countries = Destinations.objects.all()
    # print(my_countries)
    country_dict = {}
    for n, country in enumerate(my_countries):
        # print(country.country_name)
        # if country['country_name'] not in country_dict:
        country_dict[n] = {'name': country.country_name, 'been': country.been}
    countries = pd.DataFrame.from_dict(country_dict, orient='index')
    print(countries)
    my_map = folium.Map(location=[35, 0], zoom_start=1.5, zoom_control=False, control_scale=False, no_touch=True, min_zoom=2)
    folium.Choropleth(geo_data='world/json/world_countries.json',
                 name='My Countries',
                 data=countries,
                 columns=['name', 'been'],
                 key_on='feature.properties.name',
                 fill_color='BuGn',
                 nan_fill_color='white'
                ).add_to(my_map)
    my_map.save('world/templates/world/my_map.html')
    context = {
        'destinations': my_countries
    }
    return render(request, 'world/myworld.html', context)