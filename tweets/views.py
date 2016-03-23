from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from tweets.models import Tweet, HashTag
from user_profile.models import User
from tweets.forms import TweetForm

class Index(View):

    def  get(self, request):
        params = dict()
        params["name"] = "Django"
        return render(request, 'base.html', params)

    def post(self, request):
        return HttpResponse("Запрос отправлен")


class Profile(View):

    def get(self, request, username):
        params = dict()
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        form = TweetForm()
        params["tweets"] = tweets
        params["user"] = user
        params["form"] = form
        return render(request, 'profile.html', params)


class PostTweet(View):
#Tweet Post form available on page /user/<username> URL
    def post(self, request, username):
        form = TweetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(text=form.cleaned_data["text"],
                          user=user,
                          country=form.cleaned_data["country"]
                          )
            tweet.save()
            words = form.cleaned_data["text"].split(" ")
            for word in words:
                if word[0] == "#":
                    HashTag, created = HashTag.objects.get_or_create(name=word[1:])
                    HashTag.tweet.add(tweet)
        return HttpResponseRedirect("/user/" + username)
