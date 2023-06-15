from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='video/',default='')
    audio_file = models.FileField(upload_to='audio/',default='')
    # Add other fields as needed

    def __str__(self):
        return self.title
