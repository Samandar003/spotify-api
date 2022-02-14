from django.db import models

  
class Artist(models.Model):
  name = models.CharField(max_length=150, blank=False, null=False)
  picture = models.URLField(blank=True)
  def __str__(self):
    return self.name
  
class Album(models.Model):
  artist = models.ForeignKey('Artist', on_delete=models.CASCADE) # default
  title = models.CharField(max_length=150, blank=False, null=False)
  cover = models.URLField(blank=True)
  def __str__(self):
    return self.title
  
class Song(models.Model):
  album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True, blank=False)
  title = models.CharField(max_length=150, blank=False, null=False)
  cover = models.URLField(blank=True)
  source = models.URLField(blank=False, null=False)
  listened = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return self.title