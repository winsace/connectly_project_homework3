from rest_framework import serializers
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        required=True,  # Ensures the field is mandatory
        allow_blank=False,  # Prevents empty strings
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message="Username must be alphanumeric."
        )],
        error_messages={
            'blank': "Username cannot be empty.",
            'required': "Username is required."
        }
    )
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': "Email cannot be empty.",
            'required': "Email is required.",
            'invalid': "Enter a valid email address."
        }
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)

    content = serializers.CharField(
        min_length=10,
        max_length=50,
        error_messages={
            "min_length": "Post content must be at least 10 characters long.",
            "max_length": "Post content cannot exceed 50 characters.",
            "blank": "Post content cannot be empty."
        }
    )

    def validate_author(self, value):
        """Ensure author exists in the database."""
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        min_length=10,
        max_length=50,
        error_messages={
            "min_length": "Comment must be at least 10 characters long.",
            "max_length": "Comment cannot exceed 50 characters.",
            "blank": "Comment text cannot be empty."
        }
    )

    def validate_post(self, value):
        """Ensure the referenced post exists."""
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value

    def validate_author(self, value):
        """Ensure the referenced author exists."""
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']
