from rest_framework import serializers

from django.contrib.auth.models import User

from .models import GroupBlock, PrivateBlock


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class GroupBlockSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GroupBlock
        exclude = ('id', 'block')


class PrivateBlockSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PrivateBlock
        fields = ('user', 'message', 'block_thread', 'pub_date')
