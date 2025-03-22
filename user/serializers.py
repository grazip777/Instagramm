from rest_framework import serializers
from rest_framework import serializers
from .models import Subscription
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # Field only for recording

    class Meta:
        model = User
        fields = ("email", "password", "password2", "avatar", "username")

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")  # We get and delete Password2, as it is not needed to create

        # Check the length of the password
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Compare passwords
        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs

    def create(self, validated_data):
        """
        Creates a new user instance using the provided validated data.
    
        Args:
            validated_data (dict): The validated data containing user information.
    
        Returns:
            User: The newly created user instance.
        """
        # Use the create_user method provided by the User model to handle user creation
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "date_joined", "avatar")


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscript model, which displays subscribers and subscriptions.
    """

    follower = serializers.StringRelatedField(read_only=True)  # Who is signed
    following = serializers.StringRelatedField(read_only=True)  # Who is signed for

    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'following', 'subscribed_at']
