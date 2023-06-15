from django.urls import path
from App import views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', upload_video, name='upload_video'),
    path('record_video/', record_video, name='record_video'),
    path('videos/', view_all, name='view_all'),
    path('refresh-videos/', refresh_videos, name='refresh_videos'),
    path('share_link/', share_link, name='share_link'),

    path('<path:invalid_path>', error_404),

]
