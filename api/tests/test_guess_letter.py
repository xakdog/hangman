from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .mixins import CreateSession, CreateBoard
from ..models import GameScore
from ..serializers import GameBoardSerializer


class GuessWordTest(APITestCase, CreateSession, CreateBoard):
    client = APIClient()

    # TODO: test for non-existing board

    def setUp(self):
        self.board = self.create_board(
            word='metadata',
            opened='        ',
            mistakes='',
        )
        self.serialized = GameBoardSerializer(self.board)
        self.url = reverse("api:guess-letter", args=[self.board.id])

    def test_guess_whole_word(self):
        """
        Try to consequently guess whole word, duplicate symbols
        """
        expected = self.serialized.data

        sequence = [
            ('m', 'm       ', ''),
            ('a', 'm  a a a', ''),
            ('a', 'm  a a a', ''),
            ('t', 'm ta ata', ''),
            ('d', 'm tadata', ''),
            ('e', 'metadata', ''),
        ]

        expected['status'] = 'goes-on'

        for letter, opened, mistakes in sequence:
            expected['opened'] = opened
            expected['mistakes'] = mistakes
            expected['status'] = 'goes-on' if letter != 'e' else 'won'
            response = self.client.put(self.url, {'letter': letter})
            self.assertEqual(response.data, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_whole_word(self):
        """
        Try to consequently fail whole word, duplicate symbols, put after win
        """
        expected = self.serialized.data

        sequence = [
            ('7', '        ', '7'),
            ('q', '        ', '7q'),
            ('q', '        ', '7q'),
            ('p', '        ', '7qp'),
            ('o', '        ', '7qpo'),
            ('8', '        ', '7qpo8'),
            ('8', '        ', '7qpo8'),
        ]

        for letter, opened, mistakes in sequence:
            expected['opened'] = opened
            expected['mistakes'] = mistakes
            expected['status'] = 'goes-on' if letter != '8' else 'failed'
            response = self.client.put(self.url, {'letter': letter})
            self.assertEqual(response.data, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_half_word(self):
        """
        Try to consequently fail four letters, put wrong letter after win
        """
        expected = self.serialized.data

        sequence = [
            ('a', '   a a a', ''),
            ('b', '   a a a', 'b'),
            ('t', '  ta ata', 'b'),
            ('o', '  ta ata', 'bo'),
            ('e', ' eta ata', 'bo'),
            ('u', ' eta ata', 'bou'),
            ('m', 'meta ata', 'bou'),
            ('g', 'meta ata', 'boug'),
            ('d', 'metadata', 'boug'),
            ('i', 'metadata', 'boug'),
        ]

        for letter, opened, mistakes in sequence:
            expected['opened'] = opened
            expected['mistakes'] = mistakes
            expected['status'] = 'goes-on' if letter not in 'di' else 'won'
            response = self.client.put(self.url, {'letter': letter})
            self.assertEqual(response.data, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        score = GameScore.objects.first()

        self.assertEqual(GameScore.objects.count(), 1)
        self.assertEqual(score.mistakes, 4)
        self.assertEqual(score.time_spent, 0)
        self.assertEqual(score.word_length, 8)

    def test_send_invalid_symbol(self):
        """ API must return 422 error if letter is incorrect """
        letters = ['р', '!', '#', 'ab']

        expected = {
            'error': 'incorrect-letter',
            'docs': 'Letters must satisfy [a-zA-Z0-9] restrictions.'
        }

        for letter in letters:
            code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = self.client.put(self.url, {'letter': letter})
            self.assertEqual(response.data, expected)
            self.assertEqual(response.status_code, code)

    def test_strangers_state(self):
        url_create = reverse("api:board-create")

        expected = {
            "error": "no-access-to-board",
            "docs": "Use POST " + url_create +
                    " to create your own board for game.",
        }

        client = APIClient()
        client.session.create()

        response = client.put(self.url, {'letter': 'a'})
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
