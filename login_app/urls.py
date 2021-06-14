from django.urls import path
from .  import views
from . views import view_lyrics

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('home', views.home),
    path('register', views.register),
    path('login', views.login),
    path('message', views.message),
    path('search_list', views.search),
    path('add_comment/<int:id>', views.post_comment),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    #path('view_lyrics/<int:id>', views.view_lyrics),
    path('view_lyrics/<int:id>', view_lyrics ),
    path('all_time', views.all_time)
]