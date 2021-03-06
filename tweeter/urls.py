"""tweeter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from tweets.views import Index, Profile, PostTweet, HashTagCloud, Search
from user_profile.views import UserRedirect, MostFollowedUsers, Invite, InviteAccept

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^user/(\w+)/post/$', PostTweet.as_view()),
    url(r'^hashTag/(\w+)/$', HashTagCloud.as_view()),
    url(r'^$', Index.as_view()),
    url(r'^search/$', Search.as_view()),
    url(r'^search/post$', Search.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^profile/$', UserRedirect.as_view()),
    url(r'^mostFollowed/$', MostFollowedUsers.as_view()),
    url(r'^invite/$', Invite.as_view()),
    url(r'^invite/accept/(\w+)/$', InviteAccept.as_view()),
)
