from rest_framework import serializers

from .models import Post


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