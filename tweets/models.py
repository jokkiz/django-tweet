from django.db import models
from user_profile.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=160)
    created_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, null=True )
    is_active = models.BooleanField(default=True)
    TEXT_FIELD = "text"

    def __unicode__(self):
        return "tweet: {0}".format(self.text)


class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tweet = models.ManyToManyField(Tweet)

    def __unicode__(self):
        return "hash: {0}".format(self.name)
