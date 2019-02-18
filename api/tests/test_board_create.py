from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .mixins import CreateSession, CreateBoard
from ..models import GameBoard, Word
from ..serializers import GameBoardSerializer


class GameBoardTest(APITestCase, CreateSession, CreateBoard):
    client = APIClient()

    def setUp(self):
        Word.objects.bulk_create([
            Word(value="hack"),
            Word(value="python"),
            Word(value="metadata"),
        ])

    def test_successful_start(self):
        """ Check for GameSession created """
        url = reverse("api:board-create")

        response = self.client.post(url, {})
        self.assertEqual(GameBoard.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected = GameBoard.objects.first()
        serialized = GameBoardSerializer(expected)
        self.assertEqual(response.data, serialized.data)

    def test_remove_previous(self):
        """
        Previous session must be removed and new created.
        """
        old_board = self.create_board()
        self.assertEqual(GameBoard.objects.count(), 1)

        url = reverse("api:board-create")

        response = self.client.post(url, {})
        self.assertEqual(GameBoard.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_board = GameBoard.objects.first()

        self.assertNotEqual(response.data['id'], old_board.pk)
        self.assertNotEqual(new_board.word, old_board.word)

    def test_board_get(self):
        """ API must return valid board data """
        board = self.create_board()

        url = reverse("api:board-get", args=[board.pk])
        serialized = GameBoardSerializer(board)

        response = self.client.get(url)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_get_404(self):
        """ API must return 404 and some docs """
        url = reverse("api:board-get", args=[777])
        url_create = reverse("api:board-create")

        expected = {
            "error": "game-board-not-found",
            "docs": "Use POST " + url_create + " to start new game.",
        }

        response = self.client.get(url)
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_strangers_board(self):
        """ API must return 403 forbidden for non-owners """
        board = self.create_board()

        url = reverse("api:board-get", args=[board.pk])
        url_create = reverse("api:board-create")

        expected = {
            "error": "no-access-to-board",
            "docs": "Use POST " + url_create +
                    " to create your own board for game.",
        }

        client = APIClient()
        client.session.create()

        response = client.get(url)
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
