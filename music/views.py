from django.core.checks import messages
from django.db.models.query import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Song, Artist, Album
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import filters
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import TrigramSimilarity



class HelloWorldAPIView(APIView):
  def get(self, request):
    return Response(data={"message":"Hello World"})

  def post(self, request):
    message = f"Hello {request.data['name']}"
    return Response(data={"salom":message})
  
  
# class SongSerializerAPIView(APIView):
#   def get(self, request):
#     songs = Song.objects.all()
#     serial = SongSerializer(songs, many=True)
#     return Response(data=serial.data)

#   def post(self, request):
#     serial = SongSerializer(data=request.data)
#     serial.is_valid(raise_exception=True)
#     serial.save()
#     return Response(data=serial.data)
    
# class AlbumSerializerAPIView(APIView):
#   def get(self, request):
#     albums = Album.objects.all()
#     serial = AlbumSerializer(albums, many=True)
#     return Response(data=serial.data)
  
#   def post(self, request):
#     serializer = AlbumSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(data=serializer.data)

# 1-usul
class ArtistSerializerAPIView(APIView):
  def get(self, request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
  def get_object(self, request, pk):
    artist = Artist.objects.get(id=pk)
    serializer = ArtistSerializer(artist)
    return Response(serializer.data)
  def post(self, request):
    serializer = ArtistSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
  def destroy(self, request, pk):
    artist = Artist.objects.get(id=pk)
    artist.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class ArtistDetailAPIView(APIView):
  def get(self, request, pk):
    artists = Artist.objects.get(id=pk)
    serializer = ArtistSerializer(artists)
    return Response(serializer.data)

# 2-usul  
class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    
    @action(detail=True, methods=['GET'])
    def albums(self, request, *args, **kwargs):
      artist = self.get_object()
      serializer = AlbumSerializer(artist.album_set.all(), many=True)
      return Response(serializer.data)


# 3-usul
# class ArtistViewSet(viewsets.ViewSet):
#   def list(self, request):
#     queryset = Artist.objects.all()
#     serializer = ArtistSerializer(queryset, many=True)
#     return Response(serializer.data)
#   def post(self, request):
#     serializer = ArtistSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#   def retrieve(self, request, pk):
#     artist = Artist.objects.get(id=pk)
#     serializer = ArtistSerializer(artist)
#     return Response(serializer.data)
#   def put(self, request, pk):
#     artist = Artist.objects.get(id=pk)
#     serializer = ArtistSerializer(artist, data=request.data)
#     if serializer.is_valid(raise_exception=True):
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)


#   def destroy(self, request, pk):
#     artist = Artist.objects.get(id=pk)
#     artist.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
  
class AlbumViewSet(ReadOnlyModelViewSet):
  queryset = Album.objects.all()
  serializer_class = AlbumSerializer

  @action(detail=True, methods=['GET'])
  def artist(self, request, *args, **kwargs):
    album = self.get_object()
    artist = album.artist
    serializer = AlbumSerializer(artist)
    return Response(serializer.data)


class SongViewSet(ReadOnlyModelViewSet):
  queryset = Song.objects.all()
  serializer_class = SongSerializer
  # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  filter_backends = [filters.OrderingFilter, filters.SearchFilter]
  ordering_fields = ['listened', '-listened']
   # search_fields = ['^title', 'album__artist__name', 'album__title']
  def get_queryset(self):
    queryset = Song.objects.all()
    query = self.request.query_params.get('search')
    if query is not None:
      queryset = Song.objects.annotate(similarity=TrigramSimilarity
          ('title', query)).filter(similarity__gt=0.2).order_by('-similarity')
    return queryset
   
  # detail = False boganda self.get_queryset
  
  @action(detail=True, methods=['POST'])
  def listen(self, request, *args, **kwargs):
    song = self.get_object()
    with transaction.atomic():
      song.listened += 1
      song.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
  @action(detail=False, methods=['GET'])
  def top(self, request, *args, **kwargs):
    songs = self.get_queryset()
    songs = songs.order_by('-listened')[:10]
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)


  @action(detail=True, methods=['GET'])
  def albums(self, request, *args, **kwargs):
    song = self.get_object()
    serializer = AlbumSerializer(song.album_set.all(), many=True)
    return Response(serializer.data)
  
  

