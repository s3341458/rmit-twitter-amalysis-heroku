from django.db import models
from django.template.defaultfilters import default

# Create your models here.
"""
    this is the schema of tables
    please to check of the concept of object and relation mapping in order to figure out the meaning

"""


class Query(models.Model):
    searchTerm = models.TextField()
    
    
class Region(models.Model):
    regionName = models.TextField()
    latitudeBottom = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    latitudeTop = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    longtitudeBottom = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    longtitudeTop = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    def __unicode__(self):
        return self.regionName

class TweetsSentiment(models.Model):
    text = models.TextField(default = "")
    tweetID = models.BigIntegerField(default = 0,unique = True)
    tweetUserID = models.BigIntegerField(default = 0)
    sentimentLabel = models.IntegerField(default = 0)
    sentimentScore = models.FloatField(default = 0)
    lang = models.CharField(max_length=4)
    latitude = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    longtitude = models.DecimalField(null = True,max_digits=19, decimal_places=10)
    query = models.ForeignKey(Query, null=True)
    region = models.ForeignKey(Region, null=True)
    date = models.IntegerField(default = 0)
    #since 2014-5-9
    queryNum = models.IntegerField(default = 0)
    JsonString = models.TextField(default = "")
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ["tweetID"]
        





