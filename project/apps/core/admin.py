from django.contrib import admin

from apps.core.models import Profile, GradientPalette, GradientColor

admin.site.register(Profile)
admin.site.register(GradientPalette)
admin.site.register(GradientColor)
