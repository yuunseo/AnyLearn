from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User

# 회원가입 기능 구현을 위한 serializer
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # 여기서 nickname, avatar를 가져와야..하나?....음~
    class Meta:
        model = User
        fields = ("username", "birth", "phonenumber", "email", "password")


class UserRegistrationSerializer_two(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname", "avatar")

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()

        return instance


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
            "nickname",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        # 수정하면 안 될 부분
        exclude = (
            "is_superuser",
            "id",
            "is_active",
            "name",
            "groups",
            "user_permissions",
        )
