from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)  # Отображаем количество комментариев
    like_count = serializers.IntegerField(read_only=True)  # Отображаем количество лайков
    dislike_count = serializers.IntegerField(read_only=True)  # Отображаем количество дизлайков

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'author': {'required': False}
        }

    def validate(self, data):
        photo = data.get('photo')
        video = data.get('video')

        if photo and video:
            raise serializers.ValidationError('Вы не можете загрузить одновременно и фото, и видео.')

        if not photo and not video:
            raise serializers.ValidationError('Вы должны загрузить хотя бы фото или видео.')

        return data
