from mitaba.profile.models import Profile

def profile_details(backend, response, social, details, uid, user=None, *args, **kwargs):
  avatar = None

  # Facebook
  if backend.name == 'facebook':
    avatar = 'https://graph.facebook.com/v4.0/%s/picture' % response.get('id')

  # Github
  elif backend.name == 'github':
    try:
      avatar = response.get('avatar_url')
    except:
      pass

  # Google
  elif backend.name == 'google-oauth2':
    try:
      avatar = response.get('picture')
    except:
      pass

  # VK
  elif backend.name == 'vk-oauth2':
    try:
      avatar = response.get('user_photo')
    except:
      pass

  # Yandex
  elif backend.name == 'yandex-oauth2':
    try:
      avatar = 'https://avatars.yandex.net/get-yapic/%s/islands-68' % response.get('default_avatar_id')
    except:
      pass

  # Save
  if avatar:
    user.profile.avatar = avatar
    user.save()
