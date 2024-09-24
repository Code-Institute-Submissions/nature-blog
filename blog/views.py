from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from .models import Post


# class HomePage(TemplateView):
#     """
#     Displays home page
#     """
#     template_name = 'index.html'

# Create your views here.

# class based view to display the posts
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/blog.html"
    paginate_by = 6


# function-based view to show the detail of individual posts
def post_detail(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    return render(request, "blog/post_detail.html", {"post": post},)    
