from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from tweets.models import Tweet

from .forms import SignupForm
from .models import Connection, User


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/profile.html"
    model = Tweet

    def get_queryset(self):
        username = self.kwargs.get("username")
        self.profile_user = get_object_or_404(User, username=username)
        return Tweet.objects.filter(user=self.profile_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user
        context["following"] = Connection.objects.filter(follower__username=self.profile_user).count()
        context["follower"] = Connection.objects.filter(following__username=self.profile_user).count()
        context["following_user"] = Connection.objects.filter(following=self.request.user).select_related("follower")
        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        following_name = self.kwargs["username"]
        following = get_object_or_404(User, username=following_name)

        if request.user == following:
            return HttpResponseBadRequest("自分自身のユーザーをフォローすることはできません。")
        elif Connection.objects.filter(follower=self.request.user, following=following).exists():
            return HttpResponseBadRequest("既にフォローしています．")
        else:
            Connection.objects.create(follower=request.user, following=following)
            messages.success(request, f"{following.username}をフォローしました")
            return redirect("tweets:home")


class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        following_name = self.kwargs["username"]
        following = get_object_or_404(User, username=following_name)

        if following == request.user:
            return HttpResponseBadRequest("自分自身のユーザーに操作することはできません。")
        else:
            Connection.objects.filter(follower=request.user, following=following).delete()

        return redirect("tweets:home")


class FollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/following_list.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        context["following_list"] = Connection.objects.filter(follower=user).select_related("following")
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    template_name = "accounts/follower_list.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        context["follower_list"] = Connection.objects.filter(following=user).select_related("follower")
        return context
