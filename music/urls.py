from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import (
    HelloWorldAPIView, 
    SongViewSet, 
    AlbumViewSet,
    # ArtistViewSet,
    ArtistSerializerAPIView,
    ArtistDetailAPIView
)

router = DefaultRouter()
router.register('songs', SongViewSet)
router.register('albums', AlbumViewSet)
# router.register('artists', ArtistViewSet, basename='artists')

urlpatterns = [
    path('hello-world/', HelloWorldAPIView.as_view(), name='hello-world'),
    # path('artists/', ArtistAPIView.as_view(), name='artists'),
    # path('songs/', SongSerializerAPIView.as_view(), name='songs'),
    # path('albums/', AlbumSerializerAPIView.as_view(), name='album'),
    path('artists/', ArtistSerializerAPIView.as_view(), name='artists'),
    path('', include(router.urls)),
    path('artists/<int:pk>/', ArtistDetailAPIView.as_view())
]