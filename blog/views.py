from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import Post, Comment
from .forms import CommentForm


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


# function-based view to show the detail of individual posts with comments made and a form to allow comments to be added
def post_detail(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("created_on")
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Thank you, your comment has been submitted and is awaiting approval'
            )

    comment_form = CommentForm()

    return render(request, "blog/post_detail.html", 
    {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        },
        )  


# view to allow users to edit their comments
def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Thank you, your comment has been updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment! Please try again')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))       

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """       
    queryset = Post.objects.filter(status =1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Success!! Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'Sorry, you can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))  
