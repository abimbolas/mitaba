from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
# from rest_framework.schemas import get_schema_view
from mitaba.tracker import views

router = BulkRouter()
router.register(r'entries', views.EntryViewSet)
router.register(r'users', views.UserViewSet)

# schema_view = get_schema_view(title='Mitaba API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api/schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]