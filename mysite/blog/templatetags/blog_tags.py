from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_post = Post.published.order_by("-publish")[:count]
    return {"latest_post": latest_post}


@register.simple_tag
def get_most_commented_posts(count=5):
    return (
        Post.published.annotate(total_comments=Count("comments"))
        .filter(total_comments__gt=0)
        .order_by("-total_comments")[:count]
    )