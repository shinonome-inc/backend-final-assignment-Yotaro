from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
    model = Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    success_url = reverse_lazy("tweets:home")
    model = Tweet
    fields = ["content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
