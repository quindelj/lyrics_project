from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('home', views.home),
    path('all_time', views.all_time),
    path('top', views.top),
    path('search_list', views.search),
    path('view_lyrics/<int:id>', views.view_lyrics),
    
    
    path('view_profile/<int:id>', views.profile),
    path('edit_profile/<int:id>', views.edit_profile),
    path('update_profile/<int:id>', views.update_profile),
    path('profile/<int:id>/delete', views.delete_profile),

    path('create_snip/<int:id>', views.create_snippit),
    path('show_snippit/<int:snippit_id>', views.show_snippit),
    #path('edit_snippt/<int:snippot_id>', views.edit_snipppit),
    #path('update_snippit/<int:snippot_id>', views.update_snippit),
    #path('delete_snippit/<int:snippot_id>', views.delete_snippit),
    #path('like_snippit/<int:snipot_id>', views.like_snippit),
]