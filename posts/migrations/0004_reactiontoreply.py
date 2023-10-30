# Generated by Django 4.2 on 2023-10-30 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('posts', '0003_alter_reaction_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReactionToReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('reaction_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='posts.reactiontype')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.tweet')),
            ],
            options={
                'unique_together': {('reply', 'profile')},
            },
        ),
    ]
