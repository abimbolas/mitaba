from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/login/', include('rest_social_auth.urls_token')),
    url(r'^api/', include('mitaba.profile.urls')),
    url(r'^api/', include('mitaba.tracker.urls'))
]
