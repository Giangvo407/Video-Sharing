from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('videos', views.index_view, name='index'),
    path('videos/create/', views.VideoCreate.as_view(), name='video-create'),
    path('videos/<int:video_id>/', views.detail_view, name='video-detail'),
    path('videos/<int:video_id>/like/', views.like_video, name='like-video'),
    path('video/<int:pk>/update/', views.VideoUpdate.as_view(), name='video-update'),
    path('video/<int:pk>/delete/', views.VideoDelete.as_view(), name='video-delete'),
    path('video/<int:video_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('accounts/signup/', views.signup, name='signup'),
]
