from django.urls import path, include

from rest_framework_nested import routers

from blog.views import BlogViewSets
from .views import CommentViewSet

router = routers.DefaultRouter()
router.register(r'blog', BlogViewSets, basename='blog')

blog_comments_router = routers.NestedDefaultRouter(router, r'blog', lookup='blog')
blog_comments_router.register(r'comments', CommentViewSet, basename='blog-comments')

comment_replies_router = routers.NestedDefaultRouter(blog_comments_router,
                                                     r'comments', lookup='comment')
comment_replies_router.register(r'replies', CommentViewSet,
                                basename='comment-replies')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(blog_comments_router.urls)),
]