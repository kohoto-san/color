
from .models import Profile

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# import urllib2
import urllib.request


def createProfile(social_account, user):

    extra_data = social_account.extra_data

    try:
        profile = Profile.objects.get(user=user)
        is_new_profile = False
    except Profile.DoesNotExist:
        is_new_profile = True
        profile = Profile()

    profile.user = user

    if social_account.provider == "twitter":
        avatar_url = extra_data['profile_image_url']

    # if social_account.provider == "vk":
    #    avatar_url = extra_data['photo_big']

    if social_account.provider == "facebook":
        avatar_url = "http://graph.facebook.com/%s/picture?type=large" % extra_data['id']

    """
    if is_new_profile:
        try:
            id_profile = Profile.objects.all().order_by('-id_profile').first().id_profile
        except AttributeError:
            id_profile = 0
        profile.id_profile = id_profile + 1
    """

    img_format = avatar_url[-4:]

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib.request.urlopen(avatar_url).read())
    img_temp.flush()

    profile.save()

    profile.avatar.save(str(profile.user.username) + str(img_format), File(img_temp))

    return profile
