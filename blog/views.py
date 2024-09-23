from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView
from .models import Post


class HomePage(TemplateView):
    """
    Displays home page
    """
    template_name = 'index.html'

# Create your views here.

# class based view to display the posts
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "post_list.html"
