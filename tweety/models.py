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

from django.db.models import *
from django.contrib import admin

# main object
class Tweet(Model):
    message_text        = CharField(max_length=255)
    message_origin      = CharField(max_length=50)
    message_date        = DateTimeField(auto_now=True)
    message_avatar	= URLField(null=True,blank=True)
    message_media_url	= URLField(null=True,blank=True)
    message_priority    = IntegerField(default=-1)
    usernotes           = CharField(max_length=100,null=True,blank=True)
    session_id          = IntegerField(default=-1)
    message_selected    = BooleanField(default=False)
    visible             = BooleanField(default=True)
    message_status      = IntegerField(default=-1)

    def __unicode__(self):
        return u"%s" % self.message_text

# Very rudimentary admin interface
class TweetAdmin(admin.ModelAdmin):
    list_display = ( 'message_text','message_origin', 'message_date', 'visible' )
    list_editable =( 'visible', )

admin.site.register(Tweet,TweetAdmin)
