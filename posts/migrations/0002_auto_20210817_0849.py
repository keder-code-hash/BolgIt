# Generated by Django 3.2.6 on 2021-08-17 08:49

from django.db import migrations, models
import django_editorjs_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='content',
        ),
        migrations.AddField(
            model_name='posts',
            name='body_custom',
            field=django_editorjs_fields.fields.EditorJsJSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='status',
            field=models.CharField(default='', max_length=5),
        ),
    ]
