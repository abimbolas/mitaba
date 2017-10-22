from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class ProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        try:
            me = User.objects.get(pk = request.user.pk)
            avatar = resize_avatar(
                request.query_params.get('avatar_size'),
                me.profile.avatar)
            providers = list(UserSocialAuth.objects
                .filter(user=request.user)
                .values_list('provider', flat=True))
            profile = {
                'email': me.email,
                'first_name': me.first_name,
                'last_name': me.last_name,
                'avatar': avatar,
                'providers': providers
            }
            return Response(profile)
        except User.DoesNotExist:
            raise NotFound('User Not Found')


# Utils

DEFAULT_AVATAR_SIZE = 60

def resize_avatar(size, url):
    if not size:
        size = DEFAULT_AVATAR_SIZE
    return url.split('?')[0] + '?height={s}&s={s}&sz={s}'.format(s=size)
