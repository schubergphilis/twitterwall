twitterwall
===========

This twitterwall was originally developed to serve as a
'twitterwall' displaying messages from a proprietary 
messages system. It works by relaying messages from the
source system into this application.

For the devopsdays in Amsterdam, support for a real live 
twitterfeed was added. The system will still store all
tweets received over the twitter interface in a local
sqlite database (or actually any database supported
by Django).

The twitterwall has a json interface which is polled
from the browser, as well as an html based view.

On the backend, there is a simple Django admin interface
with all CRUD operations for tweets.

installation
------------
Being a django application, you'll need a system with
Django installed. There is a requirements.txt in the
root of the project to help you install Django and twitter
using pip.

It is recommended to install the project in /opt/twitterwall. If you
install it elsewhere, there are some paths in settings.py that need 
changing.

The twitterwall can be run either as a standalone application or as a wsgi
application on any webserver with wsgi support.

Use the manage.py script to:
- Configure the database: python manage.py syncdb
- Copy the static content (style sheets, javascript, html)
    python manage.py collectstatic
- Run the application standalone:
    python manage.py runserver

twitterfeed
-----------
The utils directory contains a script to pull in a feed 
of tweets from twitter (twitter_consumer.py). The script
will provide usage information when started.

The twitter credentials are stored in a separate file which
has the following format:

[auth]
class=OAuth

[auth_parameters]
token=<app token>
token_secret=<app_secret>
consumer_key=<consumer_key
consumer_secret=<consumer_secret>


Next to OAuth (which is the recommended way to authenticate), the feed
script also supports "UserPassAuth", which takes "username" and "password"
as parameters:

[auth]
class=UserPassAuth

[auth_parameters]
username=<user>
password=<pass>



