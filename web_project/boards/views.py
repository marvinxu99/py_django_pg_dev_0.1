from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Board


def boards_home(request):
    boards = Board.objects.all()
    
    return render(request, 'boards/boards.html', { 'boards': boards })

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'boards/topics.html', {'board': board})

