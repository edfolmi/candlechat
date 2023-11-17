from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('blocks/', views.blocks, name='blocks'),
    path('users/', views.candlechat_users, name='users'),

    path('block/group/<str:slug>/', views.group_block, name='block_group'),
    path('block/private/<int:other_user_id>/', views.private_block, name='block_private'),

    # ===API===
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_messages/<slug:block_slug>/', views.GroupBlockMessagesView.as_view()),
    path('private_api_messages/<int:other_user_id>/', views.PrivateBlockMessagesView.as_view()),
]
