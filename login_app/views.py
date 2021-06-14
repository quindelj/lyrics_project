from django.http import response, HttpResponseRedirect
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
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    def __init__(self: PublicAPI, time_period='day', chart_genre='all', per_page=None, page=None, text_format=None, type_='songs'):
        self.time_period='day',
        self.chart_genere='all',
        self.per_page= 20,
        self.type_='song'
        pass
    response = genius.charts(time_period='month',chart_genre='all',per_page=20)
    #print(json.dumps(['chart_item'][0], sort_keys=False, indent=4))
    return render(request, 'home.html',{'response':response})

def all_time(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    def __init__(self: PublicAPI, time_period='all_time', chart_genre='all', per_page=None, page=None, text_format=None, type_='songs'):
        self.time_period='all_time',
        self.chart_genere='all',
        self.per_page= 20,
        self.type_='song'
        pass
    response = genius.charts(time_period='all_time',chart_genre='all',per_page=20)
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
        messages.success(request, 'You have successfully registered!')
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

def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        poster = User.objects.get(id = request.session['user_id'])
        post = Comment.objects.create(comment=comment, poster= poster)
    #return redirect(f'/comment/view_lyrics/{song_id}')
    return redirect(f'/partial_comment/{post.id}')

def partial_comment(request, id):
    context = {
        'comment': Comment.objects.get(id=id)
    }
    return render(request, 'partial_comment.html', context)

def post_reply(request, song_id):
    song_id = song_id
    poster = User.objects.get(id=request.session['user_id'])
    comment = Comment.objects.get(id=id)
    Reply.objects.create(reply=request.POST['reply'], poster=poster, message=message)
    return redirect(f'{{ request.get_full_path }}')


def add_like(request, id):
    likes = Comment.objects.get(id=id)
    liked = User.objects.get(id=request.session['user_id'])
    liked.liked.add(likes)
    return redirect('/home')

def fav(request, song_id):
    #fav = song_id.get(id=id)
    #faved = User.objects.get(id=request.session['user_id'])
    #faved.faved.add(fav)
    #request.GET['song_id'] = id
    favs = Genius.objects.get_or_create(id=int(song_id))
    fav = User.objects.get(id=request.session['user_id'])
    fav.fav.add(favs)
    print (favs)
    print (faved)
    return redirect()

def profile(request, id):
    context = {
        'user':User.objects.get(id=id),
    }
    return render(request, 'profile.html', context)

def delete_comment(request, id):
    destroyed = Comments.objects.get(id=id)
    destroyed.delete()
    return redirect('/home')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
        def __init__(self: genius.search_lyrics(search_term='', per_page=None, page=None)):
            self.search_term=''
            self.per_page=10,
            self.page=2,
            
        response = genius.search(search, per_page=10, page=1)
        #print(json.dumps(response, sort_keys=False, indent=4))
        return render(request, 'search_list.html', {'response':response, 'search':search})
    

def view_lyrics(request, id):
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    
    song_id = genius.song(id )
    id = song_id['song']['id'] 
    #print(json.dumps(song_id, sort_keys=False, indent=4))
    
    lyrics = genius.lyrics(id)
    
    
    return render(request,"view_lyrics.html", {'lyrics':lyrics, 'song_id':song_id})
    




# Create your views here.
