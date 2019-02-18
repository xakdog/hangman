from django.db import models
from django.utils.timezone import now
from django.contrib.sessions.models import Session

from .managers import RandomWordManager
from .constants import MAX_WORD_LEN, MAX_MISTAKES, GAME_STATUSES


class Word(models.Model):
    value = models.CharField(max_length=MAX_WORD_LEN, unique=True)

    objects = models.Manager()
    random = RandomWordManager()

    def __str__(self):
        return "<Word: '{}' ({})>".format(self.value, self.pk)


class GameBoard(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.SmallIntegerField(choices=GAME_STATUSES)
    word = models.CharField(max_length=MAX_WORD_LEN)
    opened = models.CharField(max_length=MAX_WORD_LEN)
    mistakes = models.CharField(max_length=MAX_MISTAKES)

    def is_failed(self):
        return len(self.mistakes) >= MAX_MISTAKES

    def is_won(self):
        return not self.is_failed() and self.opened == self.word

    def is_playing(self):
        return not self.is_failed() and not self.is_won()

    def guess_letter(self, letter):
        if letter in self.word:
            self.open_letter(letter)
        else:
            self.show_mistake(letter)

    def open_letter(self, letter):
        result = ''
        for o, w in zip(self.opened, self.word):
            if w == letter:
                result += letter
            else:
                result += o
        self.opened = result

    def show_mistake(self, letter):
        if letter not in self.mistakes:
            self.mistakes += letter


class GameScore(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    mistakes = models.IntegerField()
    time_spent = models.IntegerField()
    word_length = models.IntegerField()

    @classmethod
    def from_board(cls, board: GameBoard):
        """ Create score from board """
        spent = now() - board.created_at

        return cls.objects.create(
            session=board.session,
            mistakes=len(board.mistakes),
            time_spent=spent.total_seconds(),
            word_length=len(board.word),
        )

    def calculate(self):
        return 1000 * self.word_length / (self.mistakes * (self.time_spent + 1))
