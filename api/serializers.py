from rest_framework import serializers
from .models import GameBoard


class GameBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBoard
        fields = ("id", "opened", "mistakes", "status")

    status = serializers.CharField(source='get_status_display')
