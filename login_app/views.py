from django.http import response
from django.shortcuts import render, redirect
from django.contrib import messages 
from . models import *
import lyricsgenius
from lyricsgenius.api.api import PublicAPI
import json


def index(request):
    return render (request, 'index.html')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    genius = lyricsgenius.Genius('genius token')
    def __init__(self: PublicAPI, time_period='day', chart_genre='all', per_page=None, page=None, text_format=None, type_='songs'):
        self.time_period='day',
        self.chart_genere='all',
        self.per_page= 20,
        self.type_='song'
        pass
    response = genius.charts(time_period='month',chart_genre='all',per_page=20)
    #print(json.dumps(['chart_item'][0], sort_keys=False, indent=4))
    return render(request, 'home.html',{'response':response})

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == 'GET':
        return ('/')

    errors = User.objects.basic_validator(request.POST)
    if errors:
        for(key, value) in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, 'You have successfully registures!')
        return redirect('/')
    
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/home')

def message(request):
    message = request.POST['message']
    poster = User.objects.get(id = request.session['user_id'])
    Message.objects.create(message=message, poster= poster)
    return redirect('/home')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=id)
    Comments.objects.create(comment=request.POST['comment'], poster=poster, message=message)
    return redirect('/home')


def add_like(request, id):
    likes = Message.objects.get(id=id)
    liked = User.objects.get(id=request.session['user_id'])
    liked.liked.add(likes)
    return redirect('/home')

def delete_comment(request, id):
    destroyed = Comments.objects.get(id=id)
    destroyed.delete()
    return redirect('/home')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        genius = lyricsgenius.Genius('genius token')
        def __init__(self: genius.search_lyrics(search_term='', per_page=None, page=None)):
            self.search_term=''
            self.per_page=10,
            self.page=2,
            
        response = genius.search_lyrics(search, per_page=10, page=1)
        return redirect('/search_list', {'lyric':response, 'search':search})
    
def view_lyrics(request, id):
    #problem cant seem to get target the id to diapay a selcted song
    genius = lyricsgenius.Genius('genius token')
    
    song_id = genius.song(id)
    id = [song_id['song']['id']] #if i remove this line it gives the whole api call not just the id
    #id = 6746160  if I just put an id I get stuck in a redirect loop
    
    #lyrics = genius.lyrics(id)
    #lyrics = song_lyrics.lyrics
    #response = genius.song(song_id=id)
    #print(json.dumps(request, sort_keys=False, indent=4))
    return redirect(f'/view_lyrics/{id}')




# Create your views here.
