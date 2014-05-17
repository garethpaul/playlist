sample-django-app
=================

Sample Django App for Twitter XMusic Hackathon using OAuth

REQUIREMENTS
============

To run this sample code, you'll need to install the following libraries:

- Python Social Auth, rchoi fork (https://github.com/ryankicks/python-social-auth)
- Python Twitter (https://github.com/bear/python-twitter)
- Beats Music Developer Platform SDK (https://github.com/Beats-Music/pybeats)
- Spotify Python Client (https://github.com/plamere/spotipy) 
- south (http://south.aeracode.org/)
- Fabric (http://www.fabfile.org/)

GETTING STARTED
============

- Create a Twitter App (https://apps.twitter.com/)
- Create a Beats App (https://developer.beatsmusic.com/)
- Create a Spotify App (https://developer.spotify.com/spotify-web-api/)

- Specify your Twitter App tokens in app/settings.py under the following section:

    SOCIAL_AUTH_TWITTER_KEY = 'YOUR_TWITTER_API_KEY'
    SOCIAL_AUTH_TWITTER_SECRET = 'YOUR_TWITTER_API_SECRET'
    
    TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
    TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
        
    SOCIAL_AUTH_BEATS_KEY = 'XXX'
    SOCIAL_AUTH_BEATS_SECRET = 'YYY'
    
    SOCIAL_AUTH_SPOTIFY_KEY = 'XXX'
    SOCIAL_AUTH_SPOTIFY_SECRET = 'YYY'
    
- To initialize your database, run the from the `sample-django-app` directory:

  python manage.py syncdb

- To start the server, run the following from the `sample-django-app` directory:

  fab start
  
- Open a browser and go to http://localhost:9000