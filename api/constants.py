MAX_MISTAKES = 5
MAX_WORD_LEN = 14

SYMBOLS_ALLOWED = r'^[a-zA-Z0-9]$'

GAME_STATUSES = (
    (10, 'started'),
    (20, 'goes-on'),
    (30, 'won'),
    (40, 'failed'),
)

GAME_STATUS_STARTED = 10
GAME_STATUS_GOES_ON = 20
GAME_STATUS_WON = 30
GAME_STATUS_FAILED = 40

ERR_NOT_FOUND = {
    'error': 'game-board-not-found',
    'docs': 'Use POST /api/board/ to start new game.'
}

ERR_FORBIDDEN = {
    'error': 'no-access-to-board',
    'docs': 'Use POST /api/board/ to create your own board for game.'
}

ERR_BAD_REQUEST = {
    'error': 'bad-letter-request',
    'docs': 'Use PUT /api/board/<id>/letter with {"letter": "x"} '
            'body to guess the letter.'
}

ERR_UNPROCESSABLE = {
    'error': 'incorrect-letter',
    'docs': 'Letters must satisfy [a-zA-Z0-9] restrictions.'
}
