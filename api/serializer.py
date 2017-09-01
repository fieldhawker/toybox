# coding: utf-8

from rest_framework import serializers

# from .models import User, Entry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        pass
        # model = User
        # fields = ('name', 'mail')


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        pass
        # model = Entry
        # fields = ('title', 'body', 'created_at', 'status', 'author')
