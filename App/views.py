from asyncio import Queue
import threading
from django.shortcuts import render, redirect
from .models import *
import os
import cv2
import uuid
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from .models import Video




def error_404(request, *args, **kwargs):
    return render(request, 'error_404.html', status=404)


def index(request):
    return render(request, 'index.html')


def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        title = request.POST.get('title')

        # Save the video file to the media directory
        path = default_storage.save('videos/' + video_file.name, ContentFile(video_file.read()))

        # Create a new Video object
        video = Video.objects.create(title=title, video_file=path)

        return HttpResponse('Video uploaded successfully.')
    else:
        return HttpResponse('Invalid request.')

def view_all(request):
    videos = Video.objects.all()
    return render(request, 'show_all.html',{'videos':videos})



def record_video(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')

        if action == 'record':
            # Generate a unique filename based on the current timestamp
            output_file = f'{name}.webm'
            output_path = os.path.join(settings.MEDIA_ROOT, 'video', output_file)  # Save to "media/video" folder
            print('output_path : ',output_path)

            # Save video details to the database
            video = Video(title=name, video_file=output_path)
            video.save()

            # Start recording the video
            fourcc = cv2.VideoWriter_fourcc(*'VP80')
            vid = cv2.VideoCapture(0)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
            recording = True

            while recording:
                ret, frame = vid.read()
                if ret:
                    cv2.imshow('frame', frame)
                    out.write(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Check if the request is to stop recording
                if action == 'stop':
                    recording = False

            vid.release()
            out.release()
            cv2.destroyAllWindows()

            return redirect('view_all')  # Redirect to the video list view

    return render(request, 'record_video.html')

