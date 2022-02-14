from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Song, Artist, Album
     
class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = '__all__'
  def validate_picture(self, value):
      if not value.endswith('.jpg'):
        raise ValidationError(detail='Must be .jpg file')
      return value 
  
class AlbumSerializer(serializers.ModelSerializer):
  # artist = ArtistSerializer()
  class Meta:
    model = Album
    fields = '__all__'
    
class SongSerializer(serializers.ModelSerializer):
  # album = AlbumSerializer()
  class Meta:
    model = Song
    fields = '__all__'
  def validate_title(self, value):
    if value.endswith('3'):
      raise ValidationError(detail='Must not contain 3')
    return value  
  def validate_source(self, value):
    if not value.endswith('.mp3'):
      raise ValidationError(detail='Mp3 file is required')
    return value