from django.test import TestCase
from music.models import Artist, Song, Album
from music.serializers import SongSerializer, ArtistSerializer, AlbumSerializer


class TestArtistSerializer(TestCase):
  def setUp(self) -> None:
      self.artist1 = Artist.objects.create(name='Sevinch', picture='pictures.com//profile_photos_01')
      self.artist2 = Artist.objects.create(name='shahzoda', picture='pictures.com//profile_photos_02')
      self.artist3 = Artist.objects.create(name='alibaba', picture='pictures.com//profile_photos_03')
        
  def test_data(self):
    data = ArtistSerializer(self.artist1).data
    assert data['id'] is not None
    assert data['name'] == 'Sevinch'
    assert data['picture'] == 'pictures.com//profile_photos_01'
    
    data = ArtistSerializer(self.artist2).data
    assert data['id'] is not None
    assert data['name'] == 'shahzoda'
    assert data['picture'] == 'pictures.com//profile_photos_02'
    
    data = ArtistSerializer(self.artist3).data
    assert data['id'] == 3
    assert data['name'] == 'alibaba'
    assert data['picture'] == 'pictures.com//profile_photos_03'
    
class TestSongSerializer(TestCase):
  def setUp(self) -> None:
    self.artist = Artist.objects.create(name='ibrohim', picture='pictures.com//profile_photos_05')
    self.album = Album.objects.create(artist=self.artist, title='bugungi kun')
    
  def test_is_valid(self):
    data = {
      'album':self.album.id,
      'title':'Oydin kechalar',
      'cover':'',
      'source':'https://spotify.com/one_example_song_05.mp3',
      'listened':0
    }
    serializer = SongSerializer(data=data)
    self.assertTrue(serializer.is_valid(raise_exception=True))
  
  def test_data_is_not_valid(self):
    data = {
      'title':'Bir kun kelib',
      'album':self.album.id,
      'cover':'',
      'source':'https://spotify.com/second_example_song_06',
      'listened':1
    }

    serializer = SongSerializer(data=data)
    self.assertFalse(serializer.is_valid())
    self.assertEquals(str(serializer.errors['source'][0]), 'Mp3 file is required')
          
      