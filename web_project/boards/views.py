from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


def boards_home(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html', { 'boards': boards })

def board_topics(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    return render(request, 'boards/board_topics.html', {'board': board})

@login_required
def new_topic(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():            
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
        #return redirect('boards:topic_posts', board_pk=board.pk, topic_pk=topic.pk) 
        return redirect('boards:boards_home') 
    else:
        form = NewTopicForm()

    return render(request, 'boards/new_topic.html', { 'board': board, 'form': form })

def topic_posts(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    return render(request, 'boards/topic_posts.html', { 'topic': topic })

@login_required
def reply_topic(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = PostForm()

    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})