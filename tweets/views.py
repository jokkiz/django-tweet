from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from tweets.models import Tweet, HashTag
from user_profile.models import User, UserFollower
from tweets.forms import TweetForm, SearchForm
from django.template import Context
from django.template.loader import render_to_string
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger
from tweeter import settings as s


class Index(View):

    def  get(self, request):
        params = dict()
        params["name"] = "Django"
        return render(request, 'base.html', params)

    def post(self, request):
        return HttpResponse("Запрос отправлен")


class Profile(LoginRequiredMixin, View):

    def get(self, request, username):
        params = dict()
        userProfile = User.objects.get(username=username)
        try:
            userFollower = UserFollower.objects.get(user=userProfile)
            if userFollower.followers.filter(username=request.user.username).exists():
                params["following"] = True
            else:
                params["following"] = False
        except:
            UserFollower = []

        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        tweets = Tweet.objects.filter(user=userProfile).order_by('-created_date')
        paginator = Paginator(tweets, s.TWEET_PER_PAGE)
        page = request.GET.get('page')
        try:
            tweets = paginator.page(page)
        except PageNotAnInteger:
            tweets = paginator.page(paginator.num_pages)

        params["tweets"] = tweets
        params["profile"] = userProfile
        params["form"] = form
        params["search"] = search_form
        return render(request, 'profile.html', params)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower,status = UserFollower.objects.get_or_create(user=userProfile)
        userFollower.count +=1
        if follow == True:
            userFollower.followers.add(user)
        else:
            userFollower.followers.remove(user)
        return HttpResponse(json.dumps(""), content_type='application/json')


class PostTweet(View):
    #Tweet Post form available on page /user/<username> URL
   # @permission_required('tweets.add_tweet', login_url='/login/')
    def post(self, request, username):
        form = TweetForm(self.request.POST)
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
                    hashTag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashTag.tweet.add(tweet)
        return HttpResponseRedirect("/user/" + username + "/?page=1")


class HashTagCloud(View):
    def get(self, request, hashtag):
        params = {}
        hashtag = HashTag.objects.get(name=hashtag)
        params["tweets"] = hashtag.tweet
        return render(request, 'hashtag.html', params)

class Search(View):

    def get(self, request):
        form = SearchForm()
        return render(request, 'search.html', {'search': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            tweets = Tweet.objects.filter(text__icontains=query)
            context = Context({"query": query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            return HttpResponseRedirect("/search")
