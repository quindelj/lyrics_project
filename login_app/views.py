from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages 
import lyricsgenius
from lyricsgenius.api.api import PublicAPI
import json


#log/reg

def index(request):
    context = {
        'snippits' : Snippit.objects.all()
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/register')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/login')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, "Invalid Email/Password")
        return redirect('login.html')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request,"You have successfully logged in!")
    return redirect('/login')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        context = {
        'snippits' : Snippit.objects.all()
    }
        return render(request, 'home.html', context)
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'snippits' : Snippit.objects.all()
    }
    return render(request, 'home.html', context)

#profile

def profile(request, id):
    user = User.objects.get(id=id)
    user_snippit = Snippit.objects.filter(poster=user)
    #sUser_id = User.objects.get(id=request.session['sUser_id'])
    print(user_snippit)
    return render(request, 'view_profile.html', {'user': user, 'user_snippit': user_snippit})

def edit_profile(request, id):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_profile.html', context)

def update_profile(request, id):
    edit_user = User.objects.get(id=request.session['user_id'])
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    request.session['user_id'] = edit_user.id
    return redirect(f'/edit_profile/{id}')

def delete_profile(request, id):
    delete_user = User.objects.get(id=id)
    delete_user.delete()
    return redirect('/')


#api calls

def view_lyrics(request, id):
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    if 'user_id' not in request.session:
        song_id = genius.song(id )
        id = song_id['song']['id']     
        lyrics = genius.lyrics(id)
        return render(request,"view_lyrics.html",{'lyrics':lyrics, 'song_id':song_id})
    song_id = genius.song(id )
    id = song_id['song']['id'] 
    #print(json.dumps(song_id, sort_keys=False, indent=4))
    
    lyrics = genius.lyrics(id)
    
    user = User.objects.get(id=request.session['user_id'])
    #print(lyrics)
    
    return render(request,"view_lyrics.html",{'lyrics':lyrics, 'song_id':song_id, 'user':user})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
        def __init__(self: genius.search_lyrics(search_term='', per_page=None, page=None)):
            self.search_term=''
            self.per_page=10,
            self.page=2,
        if 'user_id' not in request.session:
            response = genius.search(search, per_page=10, page=1)
            return render(request, 'search_list.html', {'response':response, 'search':search})
        response = genius.search(search, per_page=10, page=1)
        user = User.objects.get(id=request.session['user_id'])
        #print(json.dumps(response, sort_keys=False, indent=4))
        return render(request, 'search_list.html', {'response':response, 'search':search, 'user':user})

def all_time(request):
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    def __init__(self: PublicAPI, time_period='all_time', chart_genre='all', per_page=None, page=None, text_format=None, type_='songs'):
        self.time_period='all_time',
        self.chart_genere='all',
        self.per_page= 20,
        self.type_='song'
        pass
    if 'user_id' not in request.session:
        response = genius.charts(time_period='all_time',chart_genre='all',per_page=20)
        return render(request, 'charts.html',{'response':response})

    response = genius.charts(time_period='all_time',chart_genre='all',per_page=20)
    user = User.objects.get(id=request.session['user_id'])
    #print(json.dumps(['chart_item'][0], sort_keys=False, indent=4))
    return render(request, 'charts.html',{'response':response, 'user':user})

def top(request):
    genius = lyricsgenius.Genius('q3Hg0dfLarYZXLJpKIqTTQv1aF86ekG4-Dy9D8wnh8zwuykSjauy_WJ66z7oCt6L')
    def __init__(self: PublicAPI, time_period='all_time', chart_genre='all', per_page=None, page=None, text_format=None, type_='songs'):
        self.time_period='all_time',
        self.chart_genere='all',
        self.per_page= 20,
        self.type_='song'
        pass
    if 'user_id' not in request.session:
        response = genius.charts(time_period='day',chart_genre='all',per_page=20)
        return render(request, 'charts.html',{'response':response})
    
    response = genius.charts(time_period='day',chart_genre='all',per_page=20)
    user = User.objects.get(id=request.session['user_id'])
    #print(json.dumps(['chart_item'][0], sort_keys=False, indent=4))
    return render(request, 'charts.html',{'response':response, 'user':user})



#snips
def create_snippit(request):
    Snippit.objects.create(
        snippit = request.POST['snippit'],
        artist = request.POST['artist'],
        title = request.POST['title'],
        album = request.POST['album'],
        image = request.POST['image'],
        poster = User.objects.get(id=request.session['user_id'])
    )
    messages.success(request,"Snippit Created!")
    return redirect('/home')

def show_snippit(request, snippit_id):
    if 'user_id' not in request.session:
        context = {
        'snippit' : Snippit.objects.get(id=snippit_id)
    }
        return render(request, 'view_snippit.html',context)

    user =  User.objects.get(id=request.session['user_id'])
    context = {
        'snippit' : Snippit.objects.get(id=snippit_id),
        'user' : user
    }
    return render(request, 'view_snippit.html',context)
    #return render(request, 'view_snippit.html', {'user':user, 'snippit':snippit})


def like_snippit(request, id):
    if 'user_id' not in request.session:
        return render(request, 'view_snippit.html')
        
    to_like = Snippit.objects.get(id=id),
    user_like =  User.objects.get(id=request.session['user_id'])
    to_like.liked.add(user_like)
    return render('/home')

def edit_snipppit(request, snippit_id):
    context = {
        'snip': Snippit.objects.get(id=snippit_id)
    }
    return render(request, 'edit_snip.html', context)

def update_snippit(request, snippit_id):
    edit_snip = Snippit.objects.get(id=snippit_id)
    edit_snip.snippit = request.POST['snippit']
    edit_snip.artist = request.POST['artist']
    edit_snip.title = request.POST['title']
    edit_snip.album = request.POST['album']
    edit_snip.image = request.POST['image']
    edit_snip.save()
    return redirect(f'/edit_snip/{snippit_id}')

def delete_snippit(request, snippit_id):
    delete_snip = Snippit.objects.get(id=snippit_id)
    delete_snip.delete()
    return redirect('/home')