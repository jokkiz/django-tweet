from django.contrib import admin
from tweets.models import Tweet, HashTag


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_date')
    list_filter = ('user', )
    ordering = ('created_date', )
    search_fields = ('text', )


admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag)


# Register your models here.
