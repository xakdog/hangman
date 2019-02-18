from django.contrib.sessions.models import Session
from rest_framework.test import APIClient

from ..models import GameBoard
from ..constants import GAME_STATUS_STARTED


class CreateSession(object):
    client: APIClient

    def create_session(self):
        """ Start new session and return db record """
        self.client.session.create()
        key = self.client.session.session_key

        return Session.objects.get(session_key=key)


class CreateBoard(object):
    create_session: CreateSession.create_session

    def create_board(self, word='metadata', opened='me      ', mistakes='oa'):
        """ Create new dumb board. """
        session = self.create_session()
        board = GameBoard.objects.create(
            status=GAME_STATUS_STARTED,
            session=session,
            ip_address='127.0.0.1',

            word=word,
            opened=opened,
            mistakes=mistakes,
        )
        return board
