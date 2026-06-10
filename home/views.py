from django.conf import settings
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from social.apps.django_app.default.models import UserSocialAuth

import twitter
import spotipy
from pybeats.api import BeatsAPI

import re
twitter_username_re = re.compile(r'@([A-Za-z0-9_]+)', re.IGNORECASE)
tweet_id_re = re.compile(r'^[0-9]+$')
MAX_TRACK_SEARCH_LENGTH = 200

def clean_post_text(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None

def clean_tweet_id(value):
    value = clean_post_text(value)
    if value and tweet_id_re.match(value):
        return value
    return None

def clean_track_search(value):
    value = clean_post_text(value)
    if not value:
        return None
    value = twitter_username_re.sub('', value).strip()
    if not value:
        return None
    return value[:MAX_TRACK_SEARCH_LENGTH].strip() or None

def first_track_result(results):
    if not isinstance(results, dict):
        return None
    data = results.get('data')
    if not isinstance(data, list) or not data:
        return None
    track = data[0]
    if not isinstance(track, dict) or not clean_post_text(track.get('id')):
        return None
    return track

def login(request):
    
    auths = get_auths(request)
    
    if auths.get("twitter", None) and auths.get("beats", None):
        return redirect("/beats")

    context = {"request": request, "auths": auths}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def twttr(request):
    
    status = clean_post_text(request.POST.get("status", None))
    
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
    
    auth_twitter = auths.get("twitter", None)

    twitter = get_twitter(request.user)
    twitter_me = twitter.GetUser(auth_twitter.uid)

    preview = request.POST.get("preview", request.GET.get("preview", None))
    track_next = request.POST.get("track", request.GET.get("track", None))
    fav = clean_tweet_id(request.POST.get("fav", None))
    if fav:
        try:
            twitter.CreateFavorite(id=fav)
        except Exception:
            pass;
    
    # beats stuff    
    beats = get_beats(request.user)
    beats_me = beats.get_me()
    
    playlist = []
    
    statuses = twitter.GetMentions(count=100, since_id=467486341941325824)
    statuses = reversed(statuses)

    track_pair = None
    count = 0
    for s in statuses:
        if getattr(s, 'favorited', False):
            continue
        search = clean_track_search(getattr(s, 'text', None))
        if not search:
            continue
        tracks = beats.get_search_results(search, 'track', limit=1)
        
        track = first_track_result(tracks)
        if track:
            
            count = count + 1
            
            pair = [s, track]
            
            # if specified track to play, save for top of queue
            if track['id'] == track_next:
                track_pair = pair
            else:
                playlist.append(pair)
                
            if count == 5:
                break
    
    # if specified track to play, save for top of queue
    if track_pair:
        playlist.insert(0, track_pair)
    else:
        # if there's a playlist, choose first to play
        if playlist and len(playlist):
            track_pair = playlist[0]
            

    context = {"request": request, "settings": settings, 'beats': beats, "beats_me": beats_me, 'twitter': twitter, 'twitter_me': twitter_me, 'track': track_pair, 'playlist': playlist, 'preview': preview}
    return render_to_response('beats.html', context, context_instance=RequestContext(request))

from django.contrib.auth import logout as auth_logout
@login_required
@require_POST
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
        raise Exception('No user for beats API call')

    api = BeatsAPI(client_id=settings.SOCIAL_AUTH_BEATS_KEY, client_secret=settings.SOCIAL_AUTH_BEATS_SECRET)
    api.access_token = access_token

    return api

def get_auths(request):
    
    twitter = None
    beats = None

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
    
    return {'twitter': twitter, 'beats': beats}
