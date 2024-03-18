# Generated by Django 5.0.3 on 2024-03-17 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_blog_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
        migrations.AddField(
            model_name='blog',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
