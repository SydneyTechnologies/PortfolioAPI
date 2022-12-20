# Generated by Django 4.1.4 on 2022-12-20 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('projectId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.CharField(blank=True, max_length=200, null=True)),
                ('long_description', models.TextField()),
                ('thumbnail', models.URLField(blank=True, null=True)),
                ('projectGif', models.URLField(blank=True, null=True)),
                ('github_link', models.URLField(blank=True, null=True)),
                ('live_link', models.URLField(blank=True, null=True)),
                ('archive', models.BooleanField(default=False)),
                ('extra_tags', models.CharField(blank=True, max_length=200, null=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='projects.tags')),
            ],
            options={
                'verbose_name': 'project',
            },
        ),
    ]
