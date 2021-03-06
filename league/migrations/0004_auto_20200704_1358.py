# Generated by Django 3.0.3 on 2020-07-04 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_auto_20200704_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_team1', to='league.Team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_team2', to='league.Team'),
        ),
    ]
