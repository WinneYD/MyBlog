# Generated by Django 2.1.5 on 2019-03-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]