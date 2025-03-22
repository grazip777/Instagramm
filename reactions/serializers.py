from rest_framework import serializers
from .models import Like, Dislike, Post


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        request_user = validated_data.get('user')
        post = validated_data.get('post')

        # Удаляем существующий дизлайк, если он есть
        Dislike.objects.filter(user=request_user, post=post).delete()

        # Убедимся, что пользователь не ставил лайк ранее
        if Like.objects.filter(user=request_user, post=post).exists():
            raise serializers.ValidationError("Вы уже ставили лайк на этот пост.")

        # Создаём новый лайк
        return super().create(validated_data)


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'user', 'post', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        request_user = validated_data.get('user')
        post = validated_data.get('post')

        # Удаляем существующий лайк, если он есть
        Like.objects.filter(user=request_user, post=post).delete()

        # Убедимся, что пользователь не ставил дизлайк ранее
        if Dislike.objects.filter(user=request_user, post=post).exists():
            raise serializers.ValidationError("Вы уже ставили дизлайк на этот пост.")

        # Создаём новый дизлайк
        return super().create(validated_data)
