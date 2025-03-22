from rest_framework import serializers

from .models import Post, Hashtag


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Post model.
    It converts Post model instances to JSON format for API responses and validates input data for the model.
    """

    class Meta:
        model = Post
        fields = '__all__'
        # Specify additional keyword arguments for fields in the serializer.
        extra_kwargs = {
            'author': {'required': False}  # the field 'Author' is not automatically filled
        }

    def validate(self, data):
        """
        Perform additional validation to ensure that either photo or video
        is provided, but not both, or neither.
        """
        # Extract photo and video from incoming data
        photo = data.get('photo')
        video = data.get('video')

        # Rule 1: Do not allow both photo and video at the same time
        if photo and video:
            raise serializers.ValidationError('Вы не можете загрузить одновременно и фото, и видео.')

        # Rule 2: At least one of photo or video must be present
        if not photo and not video:
            raise serializers.ValidationError('Вы должны загрузить хотя бы фото или видео.')

        return data


class HashtagSerializer(serializers.ModelSerializer):
    """
    Serializer for HashTag model
    """

    class Meta:
        model = Hashtag
        fields = ['id', 'name']
