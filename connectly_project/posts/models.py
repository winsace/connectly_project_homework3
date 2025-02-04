from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class User(models.Model):
    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='Username must be alphanumeric')],
        error_messages={
            'unique': "This username is already taken. Please choose another.",
        },
        blank=False,  # Ensures username is required
        null=False
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "This email address is already in use. Please use a different one.",
        },
        blank=False,  # Ensures email is required
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField(
        blank=False,
        validators=[
            MinLengthValidator(10, message="Post content must be at least 10 characters long."),
            MaxLengthValidator(50, message="Post content cannot exceed 50 characters.")
        ],
        error_messages={
            'blank': "Post content cannot be empty.",
            'null': "Post content is required."
        }
    )
    author = models.ForeignKey(
        'User', 
        related_name='posts', 
        on_delete=models.CASCADE,
        error_messages={
            'null': "An author is required for the post.",
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField(
        blank=False,
        validators=[
            MinLengthValidator(10, message="Comment must be at least 10 characters long."),
            MaxLengthValidator(50, message="Comment cannot exceed 200 characters.")
        ],
        error_messages={
            'blank': "Comment cannot be empty.",
            'null': "Comment text is required."
        }
    )
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}: {self.text[:20]}..."
