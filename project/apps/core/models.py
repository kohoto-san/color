from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.utils import timezone

import os


@receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_logged_in_(request, user, **kwargs):
    from apps.core.utils import createProfile

    social_account = SocialAccount.objects.filter(user_id=user.id).first()

    createProfile(social_account, user)


class Profile(models.Model):

    user = models.OneToOneField(User, primary_key=True)

    def get_upload_path(instance, filename):
        return os.path.join('avatars', str(instance.user.id) + filename[-4:])

    avatar = models.ImageField(upload_to=get_upload_path, default="default.png")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username


class GradientPalette(models.Model):

    profile = models.ForeignKey(Profile)
    date = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(Profile, related_name='palette_likes', blank=True)
    likes_count = models.IntegerField(default=1)

    degrees = models.IntegerField()

    is_featured = models.BooleanField(default=False)

    def get_color_one(self):
        color = self.gradientcolor_set.filter(priority=0)[0].color
        return color

    def get_color_two(self):
        color = self.gradientcolor_set.filter(priority=1)[0].color
        return color

    def get_html(self):
        colorOne = self.gradientcolor_set.filter(priority=0)[0]
        bgOne = colorOne.color
        grad0 = str(colorOne.percentages)

        colorTwo = self.gradientcolor_set.filter(priority=1)[0]
        bgTwo = colorTwo.color
        grad100 = str(colorTwo.percentages)

        buildGradient = "(" + str(self.degrees) + "deg, " + bgOne + " " + grad0 + "%" + ", " + bgTwo + " " + grad100 + "%" + ")"

        return buildGradient

    def save(self, *args, **kwargs):

        try:
            self.likes_count = self.likes.count()
        except ValueError:
            self.likes_count = 1

        return super(GradientPalette, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "GradientPalette"
        verbose_name_plural = "GradientPalettes"

    def __str__(self):
        return str(self.id)


class GradientColor(models.Model):

    palette = models.ForeignKey(GradientPalette)
    color = models.CharField(max_length=250)
    percentages = models.IntegerField()
    priority = models.IntegerField()

    class Meta:
        verbose_name = "GradientColor"
        verbose_name_plural = "GradientColors"

    def __str__(self):
        return self.color
