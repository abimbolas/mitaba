from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
from .views import UserViewSet


router = BulkRouter()
router.register(r'users', UserViewSet)

# schema_view = get_schema_view(title='Mitaba API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api/schema/$', schema_view),
]
