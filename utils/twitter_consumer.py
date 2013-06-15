#!/usr/bin/env python
#
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
#
# consumer.py
#
# Pull in a twitterfeed and relay it to the twitterwall (Django) application

import sys
sys.path.append('/opt/twitterwall')

from argparse import ArgumentParser
from ConfigParser import ConfigParser

import os
if not "DJANGO_SETTINGS_MODULE" in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"]="settings"

from tweety.models import Tweet
from twitter import Twitter, OAuth, NoAuth, UserPassAuth, TwitterStream


# parse commandline
cmd_parser = ArgumentParser("Relay a live Twitter feed into the twitterwall")
cmd_parser.add_argument(
    "--credentials","-C",
    required=True,
    action="store",
    dest="auth",
    help="File containing twitter credentials, either oauth or username/password"
)

cmd_parser.add_argument(
    "search",
    nargs="+",
    action="store",
    help="List of keywords to search for (any keyword matched results in the tweet being matched"
)

parameters = cmd_parser.parse_args()

# parse configfile
cfg=ConfigParser()
cfg.read(parameters.auth)
auth_type = cfg.get("auth","class")
auth_parameters=dict(cfg.items("auth_parameters"))

auth_obj = locals()[auth_type](**auth_parameters)  # create instance of auth_type (class)

# main loop
stream = TwitterStream(auth=auth_obj)

for tweet in stream.statuses.filter(track=",".join(parameters.search)):

    try:
       media_url= tweet['entities']['media'][0]['media_url']
    except (KeyError,IndexError), e:
       media_url = None

    Tweet(
        message_text=tweet['text'],
        message_origin=tweet['user']['name'],
        message_avatar=tweet['user']['profile_image_url'],
        message_media_url=media_url
    ).save()

