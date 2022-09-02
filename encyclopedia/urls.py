from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # Gets home page
    path("wiki/<str:entry>", views.wiki, name="wiki"), # Gets that wiki page
    path("search", views.search, name="search"), # If there is more than one found entry, it pulls up the search page
    path("new_entry", views.new_entry, name="new_entry")
]
