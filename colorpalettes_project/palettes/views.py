from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ColorPalette, Color, PaletteRevision, FavoritePalette
from .serializers import ColorPaletteSerializer, PaletteRevisionSerializer
from django.db.models import Q
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ColorPaletteViewSet(viewsets.ModelViewSet):
    queryset = ColorPalette.objects.all()
    serializer_class = ColorPaletteSerializer

    # the create method to set the owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # action to create a palette
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.POST)
            if serializer.is_valid():
                self.perform_create(serializer)
                return render(request, 'palettes/colorpalettes_list.html')  # Redirect to the list view after successful creation
            else:
                messages.ERROR(request, 'Fill the form correctly')
                return render(request, 'palettes/colorpalettes_create.html')
        else:
            return render(request, 'palettes/colorpalettes_create.html')

    # action to get the list of palettes
    def list(self, request, *args, **kwargs):
        palettes = ColorPalette.objects.filter(
            Q(is_public=True) | Q(owner=request.user))
        return render(request, 'palettes/colorpalettes_list.html', {'palettes': palettes})

    # Custom action to update a palette
    @action(detail=True, methods=['PUT'])
    def update_palette(self, request, pk=None):
        palette = self.get_object()
        serializer = self.get_serializer(palette, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Capture revision history
        revision = PaletteRevision(
            palette=instance,
            name=instance.name,
            dominant_colors=instance.dominant_colors.all(),
            accent_colors=instance.accent_colors.all(),
        )
        revision.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    #----------Add/delete from favourite------------------
    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        palette = self.get_object()
        user = request.user
        if user.is_authenticated:
            favorite_palette, created = FavoritePalette.objects.get_or_create(user=user, palette=palette)
            if created:
                return Response({'detail': 'Palette added to favorites.'}, status=status.HTTP_200_OK)
            else:
                favorite_palette.delete()
                return Response({'detail': 'Palette removed from favorites.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    #---Search by color--------------------
    def get_result(self, request, *args, **kwargs):
        queryset = ColorPalette.objects.all()

        hex_colors = self.request.query_params.getlist('hex_color')

        if hex_colors:
            q_objects = Q()

            for hex_color in hex_colors:
                q_objects |= Q(dominant_colors__hex_value__iexact=hex_color)
                q_objects |= Q(accent_colors__hex_value__iexact=hex_color)

            queryset = queryset.filter(q_objects)

        return render(request, 'palettes/search_element.html', {'palettes': queryset})


#-------revision history-------------------------
class PaletteRevisionListView(APIView):
    def get(self, request, pk):
        palette = get_object_or_404(ColorPalette, pk=pk)
        revisions = PaletteRevision.objects.filter(palette=palette).order_by('-created_at')
        serializer = PaletteRevisionSerializer(revisions, many=True)
        return Response(serializer.data)