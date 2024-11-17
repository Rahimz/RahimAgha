from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import Post

def BlogPostView(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True, active=True)
    attachments = post.attachments.filter(active=True)
    context = dict(
        page_title=post.title,
        post=post,
        attachments=attachments,
    )
    return render(
        request,
        'blog/post_details.html',        
        context
    )


def BlogPostListView(request):
    posts = Post.actives.filter(published=True)
    context = dict(
        page_title=_("Blog"),
        posts=posts
    )
    return render(
        request,
        'blog/blog_posts.html',
        context
    )