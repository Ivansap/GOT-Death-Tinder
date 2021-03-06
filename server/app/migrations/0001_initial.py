# Generated by Django 2.0.7 on 2019-04-24 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(upload_to='card_img')),
            ],
        ),
        migrations.CreateModel(
            name='CardAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.Card')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('img', models.ImageField(upload_to='character')),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Мертв'), (2, 'Вихт'), (1, 'Жив')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('showtime', models.DateTimeField()),
                ('img', models.ImageField(upload_to='series_preview')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Вышла'), (1, 'Скоро будет')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('base_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=120)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('card_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CardAnswer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app.Character', verbose_name='Серия'),
        ),
        migrations.AddField(
            model_name='card',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app.Series', verbose_name='Серия'),
        ),
    ]
