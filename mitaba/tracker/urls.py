from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
# from rest_framework.schemas import get_schema_view
from mitaba.tracker import views

router = BulkRouter()
router.register(r'entries', views.EntryViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'auth-suka', views.AuthCodeExchange, base_name='auth-suka')

authCodeExchange = views.AuthCodeExchange.as_view()

# schema_view = get_schema_view(title='Mitaba API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth-suka/$', authCodeExchange, name="auth-suka")
    # url(r'^api/schema/$', schema_view),
]
