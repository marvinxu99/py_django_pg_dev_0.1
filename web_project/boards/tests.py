from django.test import TestCase
from django.urls import reverse, resolve

from .views import boards_home, board_topics
from .models import Board


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('boards:boards_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

def test_home_url_resolves_home_view(self):
        view = resolve('boards_home')
        self.assertEquals(view.func, boards_home)

class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django2', description='Django board.')


    def test_board_topics_view_success_status_code(self):
        url = reverse('boards:board_topics', kwargs={ 'board_id': 1 })
        print("URL=" + str(url))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('boards:board_topics', kwargs={ 'board_id': 99 })
        print("URL=" + str(url))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    # def test_board_topics_view_contains_link_back_to_homepage(self):
    #     board_topics_url = reverse('board_topics', kwargs={'pk': 1})
    #     response = self.client.get(board_topics_url)
    #     homepage_url = reverse('home')
    #     self.assertContains(response, 'href="{0}"'.format(homepage_url))


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards:boards_home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # NOT WORKING 
    # def test_home_url_resolves_home_view(self):
    #     view = resolve("boards/")
    #     self.assertEquals(view.func, boards_home)


    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'board_id': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
