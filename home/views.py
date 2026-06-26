from django.conf import settings
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from social.apps.django_app.default.models import UserSocialAuth

import twitter
import spotipy
from pybeats.api import BeatsAPI

from decimal import Decimal, InvalidOperation
import re
twitter_username_re = re.compile(r'@([A-Za-z0-9_]+)', re.IGNORECASE)
tweet_id_re = re.compile(r'^[0-9]+$')
preview_seconds_re = re.compile(r'^(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$')
MAX_TRACK_SEARCH_LENGTH = 200
MAX_PREVIEW_SECONDS_LENGTH = 16
MAX_PREVIEW_SECONDS = Decimal('3600')

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

def clean_preview_seconds(value):
    value = clean_post_text(value)
    if not value or len(value) > MAX_PREVIEW_SECONDS_LENGTH:
        return None
    if not preview_seconds_re.match(value):
        return None
    try:
        seconds = Decimal(value)
    except InvalidOperation:
        return None
    if not seconds.is_finite() or seconds > MAX_PREVIEW_SECONDS:
        return None
    return value

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

def select_playlist_track(playlist, requested_track_id):
    ordered_playlist = list(playlist)
    requested_track_id = clean_post_text(requested_track_id)
    if requested_track_id:
        for index, pair in enumerate(ordered_playlist):
            if not isinstance(pair, (list, tuple)) or len(pair) < 2:
                continue
            track = pair[1]
            if not isinstance(track, dict):
                continue
            if clean_post_text(track.get('id')) == requested_track_id:
                ordered_playlist.insert(0, ordered_playlist.pop(index))
                break
    selected_pair = ordered_playlist[0] if ordered_playlist else None
    return selected_pair, ordered_playlist

def has_required_auths(auths):
    if not isinstance(auths, dict):
        return False
    return bool(auths.get("twitter")) and bool(auths.get("beats"))

def twitter_access_tokens(extra_data):
    if not isinstance(extra_data, dict):
        return None, None
    access_token = extra_data.get('access_token')
    if not isinstance(access_token, dict):
        return None, None
    token_key = clean_post_text(access_token.get('oauth_token'))
    token_secret = clean_post_text(access_token.get('oauth_token_secret'))
    if not token_key or not token_secret:
        return None, None
    return token_key, token_secret

def beats_access_token(extra_data):
    if not isinstance(extra_data, dict):
        return None
    return clean_post_text(extra_data.get('access_token'))

def login(request):
    
    auths = get_auths(request)
    
    if has_required_auths(auths):
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
    if not has_required_auths(auths):
        return redirect("/")
    
    auth_twitter = auths.get("twitter", None)

    twitter = get_twitter(request.user)
    twitter_me = twitter.GetUser(auth_twitter.uid)

    preview = clean_preview_seconds(request.POST.get("preview", request.GET.get("preview", None)))
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
            playlist.append(pair)
                
            if count == 5:
                break
    
    track_pair, playlist = select_playlist_track(playlist, track_next)
            

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
        social_token_key, social_token_secret = twitter_access_tokens(
            getattr(usa, 'extra_data', None)
        )
        if social_token_key and social_token_secret:
            access_token_key = social_token_key
            access_token_secret = social_token_secret

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
        access_token = beats_access_token(getattr(usa, 'extra_data', None))
            
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
