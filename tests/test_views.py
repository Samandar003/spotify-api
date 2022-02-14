from django.test import TestCase, Client
from music.views import SongViewSet, ArtistViewSet, AlbumViewSet
from music.models import Artist, Song, Album


class TestArtistViewSet(TestCase):
    def setUp(self) -> None:
      self.artist = Artist.objects.create(name='Test Artist')
      self.client = Client()
    def test_get_all_albums(self):
        response = self.client.get('/artists/') 
        data = response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertIsNotNone(data[0]['id'])
        self.assertEquals(data[0]['name'], 'Test Artist')
      
class TestSongViewSet(TestCase):
    def setUp(self) -> None:
      self.artist = Artist.objects.create(name='Test Artist')
      self.album = Album.objects.create(artist=self.artist, title='Test Album')
      self.song = Song.objects.create(title='Test Song', album=self.album)
      self.client = Client()
      
    def test_song_search(self):
      response = self.client.get('/songs/?search=Test')
      data = response.data 
      self.assertEquals(response.status_code, 200)  
      self.assertEquals(len(data), 1)    
      self.assertEquals(data[0]['title'], 'Test Song')
      self.assertEquals(data[0]['album'], self.album.id)
      
      
      