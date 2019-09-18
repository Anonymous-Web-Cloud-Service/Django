# Generated by Django 2.2.5 on 2019-09-15 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_post_post_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_contents',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='space.Space'),
        ),
    ]