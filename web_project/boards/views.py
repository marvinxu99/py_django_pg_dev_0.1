from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm


def boards_home(request):
    boards = Board.objects.all()
    
    return render(request, 'boards/boards.html', { 'boards': boards })

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'boards/topics.html', {'board': board})

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
 
        return redirect('boards:board_topics', board_id=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()


    return render(request, 'boards/new_topic.html', { 'board': board, 'form': form })
