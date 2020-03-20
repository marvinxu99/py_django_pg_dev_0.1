from django.http import HttpResponse
from django.shortcuts import render

from .models import Board

def boards_home(request):
    boards = Board.objects.all()
    
    return render(request, 'boards/boards.html', { 'boards': boards })