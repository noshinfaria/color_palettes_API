from django.contrib import admin
from .models import Color, ColorPalette, FavoritePalette, PaletteRevision

admin.site.register(Color)
admin.site.register(ColorPalette)
admin.site.register(FavoritePalette)
admin.site.register(PaletteRevision)
