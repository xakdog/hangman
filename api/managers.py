from random import randint
from django.db import models
from django.db.models import Count


class RandomWordManager(models.Manager):
    def not_equal(self, skip):
        """
        Get random word not equal to `skip` parameter
        """
        for word in self.two_words():
            if word.value != skip:
                return word

    def one(self):
        """
        Get one random word from database
        """
        count = self.aggregate(count=Count('id'))['count']

        if count < 2:
            raise ValueError('not enough words')

        idx = randint(0, count - 1)

        return self.all()[idx]

    def two_words(self):
        """
        Get random range of two words from database
        """
        count = self.aggregate(count=Count('id'))['count']

        if count < 2:
            raise ValueError('not enough words')

        start = randint(0, count - 1)
        end = start + 1

        if end == count:
            start = start - 1
            end = start + 1

        return self.all()[start:end + 1]
