from django.urls import path
from App import views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', upload_video, name='upload_video'),
    path('view_all/', view_all, name='view_all'),
    path('record_video/', record_video, name='record_video'),

    path('<path:invalid_path>', error_404),

]
