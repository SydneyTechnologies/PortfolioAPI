from django.db import models
import uuid
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from rest_framework.serializers import ModelSerializer

# Create your models here.
class Projects(models.Model):

    # these are the main things that define a project
    projectId = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    long_description = models.TextField()
    thumbnail = models.URLField(max_length=200, blank=True, null=True)
    projectGif = models.URLField(max_length=200, blank=True, null=True)
    github_link = models.URLField(max_length=200, blank=True, null=True)
    live_link = models.URLField(max_length=200, blank=True, null=True)


    # other fields that are associated with relationships
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)


    # editing functionality (if the user deletes it should archive the project not actually delete it)
    archive = models.BooleanField(default=False)


    tags = models.ManyToManyField("Tags", blank=True)


    extra_tags = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "project"
        


class Tags(models.Model):
    # fields associated with a Tag
    name = models.CharField(max_length=20, unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.name 

    class Meta:
        verbose_name = "Tag"


class TestSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"

# SIGNAL DEFINITIONS
def preprocess_tag(sender, instance, **kwargs):
    # this function is responsible for making sure all tag names are saved in the write format (capitalize)
    instance.name = instance.name.replace(" ", "").capitalize()


pre_save.connect(sender=Tags, receiver=preprocess_tag)

