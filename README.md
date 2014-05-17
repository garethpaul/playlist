playlist
=================

Sample Django App for #musichackday Hackathon using Twitter X Beats API & BAM

REQUIREMENTS
============

To run this sample code, you'll need to install the following libraries:

- Python Social Auth, rchoi fork (https://github.com/ryankicks/python-social-auth)
- Python Twitter (https://github.com/bear/python-twitter  )
- Beats Music Developer Platform SDK (https://github.com/Beats-Music/pybeats)
- south (http://south.aeracode.org/)
- Fabric (http://www.fabfile.org/)

You can install them with the following command:

  pip install -r requirements.txt

GETTING STARTED
============


- Create a Twitter App (https://apps.twitter.com/)
- Create a Beats App (https://developer.beatsmusic.com/) -- Must be a paid subscription

- Specify your Twitter App tokens in app/settings.py under the following section:

    SOCIAL_AUTH_TWITTER_KEY = 'YOUR_TWITTER_API_KEY'
    SOCIAL_AUTH_TWITTER_SECRET = 'YOUR_TWITTER_API_SECRET'

    TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
    TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

    SOCIAL_AUTH_BEATS_KEY = 'XXX'
    SOCIAL_AUTH_BEATS_SECRET = 'YYY'

-- The next step of the process to run:

  pip install -r requirements.txt

- To initialize your database, run the from the `playlist` directory:

  python manage.py syncdb

- To start the server, run the following from the `playlist` directory:

  fab start

- Open a browser and go to http://localhost:9000
