from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.login),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('auth-user/', views.auth_user),

    # change password
    path('change-password/', views.change_password),

    # get user info
    path('profile/<str:pk>/', views.user_profile),

    path('', views.routes),
    path('blogs/', views.blogs),
    path('top-blogs/', views.top_blogs),
    path('blogs/<str:pk>/', views.blog),

    path('create-blog/', views.create_blog),
    path('update-blog/<str:pk>/', views.update_blog),
    path('delete-blog/<str:pk>/', views.delete_blog),

    # heart react to blog
    path('heart-blog/<str:pk>/', views.heart_blog),
    # call this url whenever view a blog
    path('views-blog/<str:pk>/', views.views_blog),
    # send comment
    path('comment-blog/<str:pk>/', views.comment_blog),
    # get comments in a blog
    path('comments-blog/<str:pk>/', views.comments_blog),
    # update and delete comment
    path('comment-update/<str:pk>/', views.comment_update),
    # categories
    path('category/', views.category),

    # delete all blogs
    path('delete-all-blogs/', views.delete_all_blogs),

    # delete account
    path('delete-account/', views.delete_account),
]