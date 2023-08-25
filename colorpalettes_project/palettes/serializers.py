from rest_framework import serializers
from .models import Color, ColorPalette, PaletteRevision


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ColorPaletteSerializer(serializers.ModelSerializer):
    dominant_colors = ColorSerializer(many=True)
    accent_colors = ColorSerializer(many=True)

    #1 to 2 dominant color(s)
    def validate_dominant_colors(self, value):
        if len(value) < 1 or len(value) > 2:
            raise serializers.ValidationError("A palette must have 1 to 2 dominant colors.")
        return value

    #2 to 4 accent colors(s)
    def validate_accent_colors(self, value):
        if len(value) < 2 or len(value) > 4:
            raise serializers.ValidationError("A palette must have 2 to 4 accent colors.")
        return value

    class Meta:
        model = ColorPalette
        fields = ['name', 'is_public', 'dominant_colors', 'accent_colors']


class PaletteRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletteRevision
        fields = '__all__'