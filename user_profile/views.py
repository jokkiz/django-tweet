from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from user_profile.models import User, UserFollower, Invitation
from user_profile.forms import InvitionForm
from tweeter import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context
import hashlib


class UserRedirect(View):
    def get(self, request):
        return HttpResponseRedirect('/user/' + request.user.username)


class MostFollowedUsers(View):
    def get(self, request):
        userFollowers = UserFollower.objects.order_by('-count')[:2]
        params = dict()
        params['userFollowers'] = userFollowers
        return render(request, 'users.html', params)


class Invite(View):
    def get(self, request):
        params = dict()
        success = request.GET.get('success')
        email = request.GET.get('email')
        invite = InvitionForm()
        params["invite"] = invite
        params["email"] = email
        params["success"] = success
        return render(request, 'invite.html', params)

    def post(self, request):
        global invitation
        form = InvitionForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = 'Invitation to join MyTweet App'
            sender_name = request.user.username
            sender_email = request.user.email
            invite_code = Invite.generate_invite_code(sender_email)
            link = 'http://%s/invite/accept/%s/' % (settings.SITE_HOST, invite_code)
            context = Context({"sender_name": sender_name, "sender_email": sender_email, "email": email, "link": link})
            invite_email_template = render_to_string('partials/_invite_email_template.html', context)
            msg = EmailMultiAlternatives(subject, invite_email_template, settings.EMAIL_HOST_USER, [email], cc=[settings.EMAIL_HOST_USER])
            user = User.objects.get(username=request.user.username)
            invitation = Invitation()
            invitation.email = email
            invitation.code = invite_code
            invitation.sender = user
            invitation.save()
            success = msg.send()

        return HttpResponseRedirect('/invite?success='+str(success)+'&email='+email)


    @staticmethod
    def generate_invite_code(email):
        secret = settings.SECRET_KEY
        email = email.encode('utf-8')
        activation_key = hashlib.sha1(secret+email).hexdigest()
        return activation_key


class InviteAccept(View):
    def get(self, request, code):
        return HttpResponseRedirect('/register?code='+code)


class Register(View):
    def get(self, request):
        params = dict()
        registration_form = RegisterForm()
        code = request.GET.get('code')
        params['code'] = code
        params['register'] = registration_form
        return render(request, 'registration/register.html', params)
        pass

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("HI")
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                print("Already registered")
            except:
                user = User()
                user.username = username
                user.email = email
                commit = True
                user = super(user, self).save(commit=False)
                user.set_password(password)
                if commit:
                    user.save()