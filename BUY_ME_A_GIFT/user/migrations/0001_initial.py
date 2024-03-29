# Generated by Django 4.1.7 on 2023-04-01 20:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True, verbose_name='IsActive')),
                ('is_admin', models.BooleanField(default=True, verbose_name='IsAdmin')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
