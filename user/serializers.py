from rest_framework import serializers
from .models import Subscription
from user.models import User

# register serializers
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2", "avatar", "username")

    def validate(self, attrs): # validation
        password = attrs.get("password")
        password2 = attrs.pop("password2")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs

    def create(self, validated_data): # create
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer): # user profile serializer
    class Meta:
        model = User
        fields = ("id", "email", "username", "date_joined", "avatar", "followers_count")


class SubscriptionSerializer(serializers.ModelSerializer): # subscription serializer
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'following', 'subscribed_at']

from rest_framework import serializers
from user.models import User


class SendAuthCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не существует.")
        return value


class VerifyAuthCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        if not user.verify_auth_code(code):
            raise serializers.ValidationError("Неверный или истёкший код аутентификации.")
        return attrs
