from django.urls import path, include
from .views import ColorPaletteViewSet,PaletteRevisionListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'palettes', ColorPaletteViewSet)


urlpatterns = [
    path('colorpalettelist/', include(router.urls), name="colorpalette-list"),

    path('colorpalettescreate/', ColorPaletteViewSet.as_view({'post': 'create'}), name='colorpalette-create'),
    path('update_palette/<int:pk>/', ColorPaletteViewSet.as_view({'put': 'update_palette'}), name='colorpalette-update'),
    path('make-favourite/<int:pk>/', ColorPaletteViewSet.as_view({'post': 'favorite'}), name='makefavourite'),
    path('palette-history/<int:pk>', PaletteRevisionListView.as_view(), name='palette-revisions'),
    path('searchlist/', ColorPaletteViewSet.as_view({'get': 'get_result'}), name='search_item'),
]