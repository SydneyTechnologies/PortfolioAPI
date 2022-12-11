# Generated by Django 4.1.4 on 2022-12-10 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_tags_options_alter_projects_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='projectId',
        ),
        migrations.AddField(
            model_name='tags',
            name='projectId',
            field=models.ManyToManyField(to='projects.projects'),
        ),
    ]