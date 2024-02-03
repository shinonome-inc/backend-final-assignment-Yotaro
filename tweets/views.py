from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView

from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
    model = Tweet
    context_object_name = "tweets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tweets"] = Tweet.objects.all()
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    success_url = reverse_lazy("tweets:home")
    model = Tweet
    fields = ["content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = Tweet


class TweetDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("tweets:home")
    model = Tweet

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user
