from django.db import models
from django.contrib.auth.models import User


class Color(models.Model):
    hex_value = models.CharField(max_length=7)


class ColorPalette(models.Model):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='palettes', on_delete=models.CASCADE)
    dominant_colors = models.ManyToManyField(Color, related_name='dominant_palettes')
    accent_colors = models.ManyToManyField(Color, related_name='accent_palettes')
    created_at = models.DateTimeField(auto_now_add=True)


class FavoritePalette(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    palette = models.ForeignKey(ColorPalette, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.palette.name}"


class PaletteRevision(models.Model):
    palette = models.ForeignKey(ColorPalette, related_name='revisions', on_delete=models.CASCADE)
    dominant_colors = models.ManyToManyField(Color, related_name='dominant_revisions')
    accent_colors = models.ManyToManyField(Color, related_name='accent_revisions')
    created_at = models.DateTimeField(auto_now_add=True)
