from django.urls import path, include
from rest_framework_nested import routers

from posts.views import (
    PaymentHistoryViewSet,
    PostViewSet,
    CommentViewSet,
    MyPostViewSet,
    initiate_payment,
    payment_fail,
    payment_success,
    payment_cancel
)

from users.views import UserProfileView, AdminUserViewSet

from friends.views import (
    FriendRequestViewSet,
    FriendshipViewSet,
    NotificationViewSet
)

# MAIN ROUTER
router = routers.DefaultRouter()

# POSTS
router.register('posts', PostViewSet, basename='posts')
router.register('my-posts', MyPostViewSet, basename='my-posts')

# USERS
router.register('profile', UserProfileView, basename='profile')
router.register('admin/users', AdminUserViewSet, basename='admin-users')

# PAYMENTS
router.register("payments", PaymentHistoryViewSet, basename="payments")

# FRIEND SYSTEM
router.register("friend-requests", FriendRequestViewSet, basename="friend-requests")
router.register("friends", FriendshipViewSet, basename="friends")
router.register("notifications", NotificationViewSet, basename="notifications")

# NESTED ROUTERS (COMMENTS)
posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

my_posts_router = routers.NestedDefaultRouter(router, 'my-posts', lookup='post')
my_posts_router.register('comments', CommentViewSet, basename='my-post-comments')


#  URL PATTERNS
urlpatterns = [

    # ALL API ROUTES
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('', include(my_posts_router.urls)),

    # AUTH (DJOSER)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # PAYMENT
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
    path("payment/fail/", payment_fail, name="payment-fail"),
]