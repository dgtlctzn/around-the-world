from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'world/home.html', {})

def world_view(request):
    return render(request, 'world/myworld.html', {})