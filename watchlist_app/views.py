from tkinter import W
from django.shortcuts import render
from watchlist_app.models import WatchList,StreamPlatform
from django.http import JsonResponse


def movie_list(request):
    movies = WatchList.objects.all()
    print(movies)
    data = {
        'movies': list(movies.values())
    }
    print(data)
    return JsonResponse(data)


def movie_details(request, pk):
    movie = WatchList.objects.get(pk=pk)
    print(movie)
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    print(data)
    return JsonResponse(data)
def home(request):
    return JsonResponse({'name':'Home page'})