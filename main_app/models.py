from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"video_id": self.id})
    

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.video}'

class LikeVideo(models.Model):
    video = models.ForeignKey(Video, related_name='likes_video', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_videos', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = [['video', 'user']]
