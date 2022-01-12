# Generated by Django 3.2 on 2022-01-12 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippit',
            name='like',
        ),
        migrations.AddField(
            model_name='snippit',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='user_like', to='login_app.User'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10)),
                ('snip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_app.snippit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_app.user')),
            ],
        ),
    ]
