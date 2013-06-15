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

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tweety.views.root_redirect'),
    url(r'^json$', 'tweety.views.json_view'),
    url(r'^getnext$', 'tweety.views.json_get_next'),
    url(r'^tweet$', 'tweety.views.new_tweet'),

    url(r'^admin/', include(admin.site.urls)),
)
