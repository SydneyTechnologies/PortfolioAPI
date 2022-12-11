from . models import Projects, Tags
from rest_framework import serializers

# this file will contain all the serializer classes

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Projects
        exclude = ["short_description"]
    
       

    def create(self, validated_data):
        extra_tags = validated_data.pop("extra_tags")
        current_tags = validated_data.pop("tags")
        if extra_tags:
            extra_tags = extra_tags.split(",")

        project = Projects.objects.create(**validated_data)
        for tags in extra_tags:
            if tags.capitalize() in [i.name for i in Tags.objects.all()]: 
                tag = Tags.objects.get(name = tags.capitalize())
            else:
                tag = Tags.objects.create(name = tags.capitalize())
            project.tags.add(tag)
        project.tags.add(current_tags)
        return project
        
    def update(self, instance, validated_data):
        extra_tags = validated_data.pop("extra_tags")
        current_tags = instance.tags.all()
        new_tags = []
        if extra_tags:
            extra_tags = extra_tags.split(",")

            for tags in extra_tags:
                tag, created = Tags.objects.get_or_create(name = tags.replace(" ", "").capitalize())
                print(tag, created)

                if not tag in current_tags:
                    new_tags.append(tag)
            validated_data.update({"tags":[*current_tags, *new_tags]})
        else:
            validated_data.update({"extra_tags":None})
            

        return super().update(instance, validated_data)

