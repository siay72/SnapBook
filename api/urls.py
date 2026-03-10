from django.urls import path, include
from rest_framework_nested import routers
from posts.views import (    PaymentHistoryViewSet,
    PostViewSet,
    CommentViewSet,
    MyPostViewSet,
    initiate_payment,
    payment_fail,
    payment_success,
    payment_cancel )
from users.views import UserProfileView, AdminUserViewSet

router = routers.DefaultRouter()

router.register('posts', PostViewSet, basename='posts')
router.register('profile', UserProfileView, basename='profile')
router.register('my-posts', MyPostViewSet, basename='my-posts')
router.register('admin/users', AdminUserViewSet, basename='admin-users')
router.register("payments", PaymentHistoryViewSet, basename="payments")

posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

my_posts_router = routers.NestedDefaultRouter(router, 'my-posts', lookup='post')
my_posts_router.register('comments', CommentViewSet, basename='my-post-comments')





urlpatterns = [

    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('', include(my_posts_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
    path("payment/fail/", payment_fail, name="payment-fail"),
]
