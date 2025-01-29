from django.urls import path
from .views import video_list, video_create, video_share, video_trim, video_merge, video_access

urlpatterns = [
    path('list/', video_list, name='video_list'),
    path('create/', video_create, name='video_create'),
    path('<int:video_id>/share/', video_share, name='video_share'),
    path('<int:video_id>/trim/', video_trim, name='video_trim'),
    path('merge/', video_merge, name='video_merge'),
    # path('upload/', upload_video, name='video_upload'),
    path("<uuid:unique_id>/", video_access, name="video_access"),
]
