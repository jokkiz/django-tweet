from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from user_profile.models import User, UserFollower


class UserRedirect(View):
    def get(self, request):
        return HttpResponseRedirect('/user/' + request.user.username)


class MostFollowedUsers(View):
    def get(self, request):
        userFollowers = UserFollower.objects.order_by('-count')[:2]
        params = dict()
        params['userFollowers'] = userFollowers
        return render(request, 'users.html', params)