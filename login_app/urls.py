from django.urls import path
from .  import views
from . views import view_lyrics

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('home', views.home),
    path('register', views.register),
    path('login', views.login),
    path('comment', views.comment),
    path('search_list', views.search),
    path('post_reply/<int:id>', views.post_reply),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('view_lyrics/<int:id>', views.view_lyrics),
    path('profile/<int:id>', views.profile),
    path('all_time', views.all_time),
    path('fav/<int:song_id>', views.fav),
    path('partial_comment/<int:id>', views.partial_comment)
]