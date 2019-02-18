import re

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GameBoard, GameScore, Word
from .serializers import GameBoardSerializer
from .constants import ERR_NOT_FOUND, ERR_FORBIDDEN, ERR_BAD_REQUEST, \
    ERR_UNPROCESSABLE, SYMBOLS_ALLOWED, GAME_STATUS_STARTED, \
    GAME_STATUS_GOES_ON, GAME_STATUS_FAILED, GAME_STATUS_WON


@api_view(['GET'])
def board_get(request, pk=None):
    """ Get game state """
    try:
        board = GameBoard.objects.get(pk=pk)
    except GameBoard.DoesNotExist:
        return Response(ERR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    if request.session.session_key != board.session.session_key:
        return Response(ERR_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)

    serialized = GameBoardSerializer(board)

    return Response(serialized.data)


@api_view(['POST'])
def board_create(request):
    """ Start the game, drop existing board if needed """
    if not request.session.session_key:
        request.session.create()

    previous = None
    session = Session.objects.get(session_key=request.session.session_key)

    try:
        board = GameBoard.objects.get(session=session)
        previous = board.word
        board.delete()
    except GameBoard.DoesNotExist:
        pass

    client_ip = request.META['REMOTE_ADDR']

    word = Word.random.not_equal(previous) if previous else Word.random.one()
    places = ' ' * len(word.value)

    board = GameBoard.objects.create(
        session=session,
        ip_address=client_ip,
        status=GAME_STATUS_STARTED,
        word=word.value,
        opened=places,
        mistakes='',
    )
    serialized = GameBoardSerializer(board)

    return Response(serialized.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def guess_letter(request, pk=None):
    """ Try to guess letter on board """
    try:
        board = GameBoard.objects.get(pk=pk)
    except GameBoard.DoesNotExist:
        return Response(ERR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    if request.session.session_key != board.session.session_key:
        return Response(ERR_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)

    if 'letter' not in request.data:
        return Response(ERR_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    letter = request.data.get('letter')

    if not re.match(SYMBOLS_ALLOWED, letter):
        return Response(ERR_UNPROCESSABLE, status.HTTP_422_UNPROCESSABLE_ENTITY)

    if board.is_playing():
        board.guess_letter(letter)
        board.status = GAME_STATUS_GOES_ON

    if board.is_failed():
        board.status = GAME_STATUS_FAILED

    if board.is_won() and board.status == GAME_STATUS_GOES_ON:
        GameScore.from_board(board).save()
        board.status = GAME_STATUS_WON

    board.save()

    state = GameBoardSerializer(board)

    return Response(state.data, status=status.HTTP_200_OK)
