from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.utils import timezone

import os
import hashlib


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


class Color(models.Model):

    color = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.color


class PaletteMeta(models.Model):

    profile = models.ForeignKey(Profile, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(Profile, related_name='%(class)s_likes', blank=True)
    likes_count = models.IntegerField(default=1)

    is_featured = models.BooleanField(default=False)
    date_featured = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):

        try:
            self.likes_count = self.likes.count()
        except ValueError:
            self.likes_count = 1

        if self.is_featured and self.date_featured is None:
            self.date_featured = self.date

        return super(PaletteMeta, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ColorPalette(PaletteMeta):

    colors = models.ManyToManyField(Color, related_name='palette_colors', blank=True)

    def get_colors(self):
        return self.colors.through.objects.filter(colorpalette=self)
        # return self.colors.through.objects.all()

    class Meta:
        verbose_name = "ColorPalette"
        verbose_name_plural = "ColorPalettes"

    def __str__(self):
        return str(self.id)


class ImagePalette(PaletteMeta):

    colors = models.ManyToManyField(Color, related_name='image_colors', blank=True)
    original_url = models.URLField(null=True)

    def get_colors(self):
        return self.colors.through.objects.filter(imagepalette=self)

    def get_upload_path(instance, filename):
        pos_img_format = filename.rfind('.')
        img_format = filename[pos_img_format:]

        m = hashlib.sha1()
        image_id = str(instance.id).encode('utf-8')
        m.update(image_id)
        return os.path.join('image', m.hexdigest() + img_format)

    image = models.ImageField(upload_to=get_upload_path)

    class Meta:
        verbose_name = "ImagePalette"
        verbose_name_plural = "ImagePalettes"

    def __str__(self):
        return str(self.id)


class GradientPalette(models.Model):

    profile = models.ForeignKey(Profile, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(Profile, related_name='gradient_likes', blank=True)
    likes_count = models.IntegerField(default=1)

    degrees = models.IntegerField()

    is_featured = models.BooleanField(default=False)
    date_featured = models.DateTimeField(blank=True, null=True)

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

        if self.is_featured and self.date_featured is None:
            self.date_featured = self.date

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
