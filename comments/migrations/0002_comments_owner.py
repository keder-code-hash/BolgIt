# Generated by Django 3.0.7 on 2021-05-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='owner',
            field=models.ManyToManyField(to='users.Register'),
        ),
    ]
