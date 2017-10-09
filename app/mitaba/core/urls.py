from django.conf.urls import include, url
from django.contrib import admin
from mitaba.core.settings import DEBUG

urlpatterns = [
    url(r'^api/login/', include('rest_social_auth.urls_token')),
    url(r'^api/', include('mitaba.profile.urls')),
    url(r'^api/', include('mitaba.tracker.urls'))
]

# Show public admin only in development
if DEBUG is True:
  urlpatterns += [url(r'^admin/', admin.site.urls)]
