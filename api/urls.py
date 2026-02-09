from django.urls import path, include
from rest_framework_nested import routers
from posts.views import PostViewSet, CommentViewSet
from users.views import UserProfileView

router = routers.DefaultRouter()

router.register('posts', PostViewSet, basename='posts')
router.register('profile', UserProfileView, basename='profile')



posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')







urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
