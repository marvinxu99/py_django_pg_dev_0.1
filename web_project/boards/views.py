from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


def boards_home(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html', { 'boards': boards })

def board_topics(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # genearte a replies 'column' on the fly
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'boards/board_topics.html', { 'board': board, 'topics': topics })

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
    topic.views += 1
    topic.save()
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


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    # Overriding the get_queryset method of the UpdateView - so other users can not edit the post.
    # This also fixed UnauthorizedPostUpdateViewTests.test_status_code issue with 200 != 404
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)