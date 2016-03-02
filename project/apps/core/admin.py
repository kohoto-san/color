from django.contrib import admin

from apps.core.models import Profile, GradientPalette, GradientColor, Color, ColorPalette, ImagePalette

admin.site.register(Profile)
admin.site.register(GradientPalette)
admin.site.register(GradientColor)

admin.site.register(Color)
admin.site.register(ColorPalette)
admin.site.register(ImagePalette)
