from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "api"

urlpatterns = [
    path('board/', views.board_create, name='board-create'),
    path('board/<int:pk>', views.board_get, name='board-get'),
    path('board/<int:pk>/letter/', views.guess_letter, name='guess-letter'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
