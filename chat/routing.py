from django.urls import path
from .block_group_consumers import GroupBlockConsumer
from .block_private_consumers import PrivateBlockConsumer


websocket_urlpatterns = [
    path('ws/block/<str:slug>/', GroupBlockConsumer.as_asgi()),
    path('ws/privateblock/<int:userId>/', PrivateBlockConsumer.as_asgi())
]
