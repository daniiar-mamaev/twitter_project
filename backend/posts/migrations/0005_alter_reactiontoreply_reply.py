# Generated by Django 4.2 on 2023-10-30 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_reactiontoreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactiontoreply',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.reply'),
        ),
    ]
