from django.contrib import admin
from tweets.models import Tweet, HashTag

admin.site.register(Tweet)
admin.site.register(HashTag)


def __unicode__(self):
    return self.text
# Register your models here.
