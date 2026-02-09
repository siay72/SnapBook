from django.urls import path, include
from rest_framework_nested import routers
from posts.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()

router.register('posts', PostViewSet, basename='posts')
posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')




urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
