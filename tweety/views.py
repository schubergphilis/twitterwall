#   Copyright 2013 Gert Kremer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from tweety.models import Tweet
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import *
from django.utils.datastructures import MultiValueDictKeyError 
from django.contrib.auth.decorators import login_required,permission_required
from basic_auth import *

def param(req,param):
    try:
        return req.GET[param]
    except (IndexError,MultiValueDictKeyError):
        return None


def root_view(req):
    """
    render last 'limit' tweets using main.html template
    """
    try:
        limit = int(param(req,"limit"))
    except:
        limit = 40

    tweets = Tweet.objects.filter(visible=True).order_by("-message_date")[0:limit]
    return render_to_response('tweety/main.html', { "tweets" : tweets } )

def root_redirect(req):
    return(redirect("/static/twitterwall.html",permanent=True))


def json_view(req):
    try:
        limit = int(param(req,"limit"))
    except:
        limit = 40

    tweets = Tweet.objects.filter(visible=True).order_by("-pk")[0:limit]
    result = HttpResponse(mimetype="application/json")
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(tweets, ensure_ascii=False, stream=result)
    return result

def json_get_next(req):
    last_displayed = int(param(req,"item"))

    tweets = Tweet.objects.filter(visible=True).filter(pk__gt=last_displayed)[0:1]
    result = HttpResponse(mimetype="application/json")
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(tweets, ensure_ascii=False, stream=result)
    return result



@has_perm_or_basicauth("tweety.add_tweet")
def new_tweet(req):
    username = param(req,"username")
    message = param(req,"message")
    usernotes = param(req,"notes")
    try:
        selected  = param(req,"selected").upper()[0]
    except:
        selected = None

    if selected in [ 'Y','J','T' ]:
        selected = True
    else:
        selected = False


    # TODO: check request.META["USERNAME"] and has_perm(user,'tweety.add_tweet'), 
    #       return permission denied if failed. The decorators perform undesired
    #       redirect magic

    result = HttpResponse(mimetype="text/plain")
    try:
        tweet = Tweet(
                    message_text=message,
                    message_origin=username,
                    message_selected=selected,
                    usernotes=usernotes
        )
        tweet.save()
        result.write("OK")
    except:
        result.write("FAILED")

    return result        # we may want to just return "OK"
