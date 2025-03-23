from rest_framework import serializers
from .models import Subscription
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2", "avatar", "username")

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "date_joined", "avatar", "followers_count")


class SubscriptionSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'following', 'subscribed_at']
