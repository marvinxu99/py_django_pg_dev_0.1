from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


# def boards_home(request):
#     boards = Board.objects.all()
#     return render(request, 'boards/boards_home.html', { 'boards': boards })
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/boards_home.html'


def board_topics(request, board_pk):
    '''
    Pagination using the regular function-based views (FBV)
    See below for Generic Class-Based View (GCBV) pagination
    '''
    board = get_object_or_404(Board, pk=board_pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
  
    return render(request, 'boards/board_topics_fbv.html', { 'board': board, 'topics': topics })


class TopicListView(ListView):
    '''
    Generic Class-Based View (GCBV) pagination
    See above for pagination using the regular function-based views (FBV)

    While using pagination with class-based views, the way we interact with the paginator in the 
    template is a little bit different. It will make available the following variables in the 
    template: paginator, page_obj, is_paginated, object_list, and also a variable with the name 
    we defined in the context_object_name. In our case this extra variable will be named topics, 
    and it will be equivalent to object_list.

    Now about the whole get_context_data thing, well, that’s how we add stuff to the request 
    context when extending a GCBV
    '''
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/board_topics.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


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


# def topic_posts(request, board_pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'boards/topic_posts.html', { 'topic': topic })
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


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