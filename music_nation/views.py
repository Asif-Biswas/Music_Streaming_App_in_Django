from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
    )
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate
from .forms import SignUpForm
from .models import Album, Song
from .forms import NewAlbum, NewSong
from django.contrib import messages

##########################################################

def home(request):
    #show all albums in chronological order of it's upload
    albums = Album.objects.all()
    return render(request, 'music_nation/homepage.html',{'albums':albums})


def home2(request):
    #show all albums in chronological order of it's upload
    albums = Album.objects.all()
    first_album = albums[0]
    songs = Song.objects.filter(song_album=first_album)
    songs_json = []
    for song in songs:
        songs_json.append({'name':song.song_name, 'url':song.song_file.url, 'album':song.song_album.album_name})
    return render(request, 'music_nation/index.html',{'albums':albums, 'songs':songs_json, 'first_album':first_album})

#........................................................#

def profile_detail(request, username):
    # show all albums of the artist
    albums = Album.objects.filter(album_artist__username=username)
    return render(request, 'music_nation/artist.html', {'albums':albums, 'username':username})

#........................................................#

@login_required
def add_album(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        print(logo)
        album = Album.objects.create(
            album_name=name,
            album_logo=logo,
            album_genre=genre,
            album_artist=request.user
        )
        album.save()
        return redirect('music_nation:profile_detail', username=request.user.username)

    return render(request, 'music_nation/add_album.html')

#........................................................#

def album_detail(request,username, album):
    #show album details here. single album's details.
    album = get_object_or_404(Album, album_name=album)
    songs = get_object_or_404(User, username=username)
    songs = songs.albums.get(album_name=str(album))
    songs = songs.songs.all()
    songs_json = []
    for song in songs:
        songs_json.append({'name':song.song_name, 'url':song.song_file.url, 'album':song.song_album.album_name})

    albums = Album.objects.all()
    return render(request, 'music_nation/index.html',{'albums':albums, 'songs':songs_json, 'first_album':album})

#........................................................#

def signup(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username= request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('music_nation:signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('music_nation:signup')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('music_nation:signup')
        
        if len(password) < 6:
            messages.error(request, 'Password must be atleast 6 characters long.')
            return redirect('music_nation:signup')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        login(request, user)
        return redirect('music_nation:home')
    
    return render(request, 'music_nation/signup.html')


def loginHandler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('music_nation:home')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            messages.error(request, 'Invalid login details supplied.')
            
    return render(request, 'music_nation/login.html')
#........................................................#

@login_required
def delete_album(request, username, album):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        album_to_delete = get_object_or_404(User, username=username)
        album_to_delete = album_to_delete.albums.get(album_name=album)
        song_to_delete = album_to_delete.songs.all()
        for song in song_to_delete:
            song.delete_media()#deletes the song_file
        album_to_delete.delete_media()#deletes the album_logo
        album_to_delete.delete()#deletes the album from database
        return redirect('music_nation:profile_detail', username=username)
    else:
        return redirect('music_nation:profile_detail', username=username)

#........................................................#

@login_required
def add_song(request, username, album):

    user = get_object_or_404(User, username=username)

    if request.user == user:

        album_get = Album.objects.get(album_name=album)

        if request.method == 'POST':
            name = request.POST.get('name')
            song_file = request.FILES.get('file')
            song = Song.objects.create(
                song_name=name,
                song_file=song_file,
                song_album=album_get
            )
            song.save()
            return redirect('music_nation:album_detail', username=username, album=album)

        
        return render(request, 'music_nation/add_song.html', {'album':album, 'username':username})
    
    else:
        return redirect('music_nation:profile_detail', username=username)
