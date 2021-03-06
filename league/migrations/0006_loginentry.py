# Generated by Django 3.0.3 on 2020-07-05 03:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0005_auto_20200704_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_login', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
