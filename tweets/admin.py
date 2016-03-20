from django.contrib import admin
from tweets.models import Tweet

admin.site.register(Tweet)

def __unicode__(self):
    return self.text
# Register your models here.
