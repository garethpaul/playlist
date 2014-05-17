from django.conf import settings
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth

import twitter
import spotipy
from pybeats.api import BeatsAPI

import re
twitter_username_re = re.compile(r'@([A-Za-z0-9_]+)', re.IGNORECASE)

def login(request):
    
    auths = get_auths(request)
    
    if auths.get("twitter", None) and auths.get("beats", None):
        return redirect("/beats")

    context = {"request": request, "auths": auths}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def twttr(request):
    
    status = request.REQUEST.get("status", None)
    
    api = get_twitter(request.user)
    if status:
        api.PostUpdates(status)
    
    statuses = api.GetUserTimeline(screen_name=request.user.username, count=10)
    
    context = {"request": request, "settings": settings, 'api': api, 'statuses': statuses}
    return render_to_response('twitter.html', context, context_instance=RequestContext(request))

@login_required
def beats(request):
    
    auths = get_auths(request)
    if not auths.get("twitter", None) or not auths.get("beats", None):
        return redirect("/login")

    twitter = get_twitter(request.user)

    trackNext = request.REQUEST.get("track", None)
    fav = request.REQUEST.get("fav", None)
    if fav:
        try:
            twitter.CreateFavorite(id=fav)
        except:
            pass;
    
    # beats stuff    
    beats = get_beats(request.user)
    beats_me = beats.get_me()
    
    playlist = []
    
    statuses = twitter.GetMentions(count=40)
#     statuses = []
    track_pair = None
    count = 0
    for s in statuses:
        if s.favorited:
            continue
        search = twitter_username_re.sub('', s.text)
        tracks = beats.get_search_results(search, 'track', limit=1)
        
        if tracks and len(tracks['data']) > 0:
            
            count = count + 1
            
            track = tracks['data'][0]
            pair = [s, track]
            
            # if specified track to play, save for top of queue
            if track['id'] == trackNext:
                track_pair = pair
            else:
                playlist.insert(0, pair)
                
            if count == 5:
                break
    
    # if specified track to play, save for top of queue
    if track_pair:
        playlist.insert(0, track_pair)
    else:
        # if there's a playlist, choose first to play
        if playlist and len(playlist):
            track_pair = playlist[0]
    
    context = {"request": request, "settings": settings, 'beats': beats, "beats_me": beats_me, 'twitter': twitter, 'track': track_pair, 'playlist': playlist}
    return render_to_response('beats.html', context, context_instance=RequestContext(request))

@login_required
def spotify(request):

    auths = get_auths(request)
    if not auths.get("twitter", None) or not auths.get("spotify", None):
        return redirect("/login")
    
    status = request.REQUEST.get("status", None)
    
    api = get_spotify(request.user)
    
    me = api.me()
    
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
    artist = api.artist(urn)
    
    playlists = api.user_playlists(me['id'])
    
    playlist_id = playlists['items'][0]['uri']
    playlist = api.playlist(playlist_id)
    
    context = {"request": request, "settings": settings, 'api': api, 'me': me, 'artist': artist, "playlists": playlists}
    return render_to_response('spotify.html', context, context_instance=RequestContext(request))

from django.contrib.auth import logout as auth_logout
def logout(request):
    """Logs out user"""

    user = request.user

    auth = UserSocialAuth.objects.filter(user=user)
    for a in auth:
        a.delete()
    
    auth_logout(request)
    return HttpResponseRedirect('/')

def get_twitter(user):

    access_token_key = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    usa = UserSocialAuth.objects.get(user=user, provider='twitter')
    if usa:
        access_token = usa.extra_data['access_token']
        if access_token:
            access_token_key = access_token['oauth_token']
            access_token_secret = access_token['oauth_token_secret']

    if not access_token_key or not access_token_secret:
        raise Exception('No user for twitter API call')

    api = twitter.api.Api(
        base_url='https://api.twitter.com/1.1',
        consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
        consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

    return api

def get_beats(user):

    access_token = None
    usa = UserSocialAuth.objects.get(user=user, provider='beats')
    if usa:
        access_token = usa.extra_data['access_token']
            
    if not access_token:
        raise Exception('No user for spotify API call')

    api = BeatsAPI(client_id=settings.SOCIAL_AUTH_BEATS_KEY, client_secret=settings.SOCIAL_AUTH_BEATS_SECRET)
    api.access_token = access_token

    return api

def get_spotify(user):

    access_token = None
    usa = UserSocialAuth.objects.get(user=user, provider='spotify')
    if usa:
        access_token = usa.extra_data['access_token']
            
    if not access_token:
        raise Exception('No user for spotify API call')

    api = spotipy.Spotify(access_token)

    return api

def get_auths(request):
    
    twitter = None
    beats = None
    spotify = None

    if request.user and request.user.is_authenticated():
        user = request.user
        try:
            twitter = UserSocialAuth.objects.get(user=user, provider='twitter')
        except UserSocialAuth.DoesNotExist:
            pass
        
        try:
            beats = UserSocialAuth.objects.get(user=user, provider='beats')
        except UserSocialAuth.DoesNotExist:
            pass
    
        try:
            spotify = UserSocialAuth.objects.get(user=user, provider='spotify')
        except UserSocialAuth.DoesNotExist:
            pass      
        
    return {'twitter': twitter, 'beats': beats, 'spotify': spotify}
