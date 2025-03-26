from rest_framework import serializers

from .models import Post

# Пост

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'likes_count', 'dislikes_count', 'comments_count', 'created_at',
                  'updated_at']


    def validate(self, data):
        photo = data.get('photo')
        video = data.get('video')

        if photo and video:
            raise serializers.ValidationError('Вы не можете загрузить одновременно и фото, и видео.')

        if not photo and not video:
            raise serializers.ValidationError('Вы должны загрузить хотя бы фото или видео.')

        return data
