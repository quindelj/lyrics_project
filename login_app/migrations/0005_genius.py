# Generated by Django 3.2 on 2021-06-14 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0004_lyric'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genius',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.ManyToManyField(related_name='fav', to='login_app.User')),
            ],
        ),
    ]
