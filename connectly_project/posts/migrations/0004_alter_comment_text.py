# Generated by Django 5.1.5 on 2025-02-03 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_author_alter_post_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(error_messages={'blank': 'Comment cannot be empty.', 'null': 'Comment text is required.'}, validators=[django.core.validators.MinLengthValidator(10, message='Comment must be at least 10 characters long.'), django.core.validators.MaxLengthValidator(50, message='Comment cannot exceed 200 characters.')]),
        ),
    ]
