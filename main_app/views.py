from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Video, Comment, LikeVideo
from .forms import CommentForm

def index_view(request):
    videos = Video.objects.all()
    context = {
        'videos': videos
    }
    return render(request, 'videos/index.html', context)

def detail_view(request, video_id):
    video = Video.objects.get(id=video_id)
    comments = video.comments.all()
    likes = video.likes_video.filter(is_like=True).count()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return redirect('video-detail', video_id=video_id)
    else:
        form = CommentForm()
    
    context = {
        'video': video,
        'comments': comments,
        'likes': likes,
        'form': form
    }
    return render(request, 'videos/detail.html', context)

@login_required
def like_video(request, video_id):
    video = Video.objects.get(id=video_id)
    user = request.user
    existing_like = LikeVideo.objects.filter(video=video, user=user, is_like=True).first()
    if existing_like:
        existing_like.delete()
    else:
        LikeVideo.objects.create(video=video, user=user, is_like=True)
    
    return redirect('video-detail', video_id=video_id)

@login_required
def delete_comment(request, video_id, comment_id):
    video = Video.objects.get(id=video_id)
    comment = video.comments.all()
    comment.delete()
    return redirect('video-detail', video_id=video_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

class VideoCreate(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'video_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class VideoUpdate(LoginRequiredMixin, UpdateView):
    model = Video
    fields = ['title']

class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video
    success_url = '/videos'

class Home(LoginView):
    template_name = 'home.html'