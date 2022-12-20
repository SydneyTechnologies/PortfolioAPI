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
        # the to add list will contain all the tags that are to be added to this 
        # specific project
        toAdd = []
        if extra_tags:
            extra_tags = extra_tags.split(",")
            print(extra_tags)
            for tags in set(extra_tags):
                # we get the tags if the exist already if not we create them
                target = tags.replace(" ", "").capitalize()
                tag, created = Tags.objects.get_or_create(name = target)
                # now let us append these tags to the toAdd list
                toAdd.append(tag)

        

        print(f"this is the current tags to add {current_tags} and the type {type(current_tags)}")
        print(f"these are the extra tags {extra_tags} ")

        if current_tags:
            print(f"the list is not empty {current_tags} the length {len(current_tags)}")
            # so add the current_tags to the list (toAdd list)
            toAdd = toAdd + current_tags 
        
        # so we need to make all entires in the toAdd list unique
        toAdd = set(toAdd)
        project = Projects.objects.create(**validated_data)
        print("THIS IS THE FOCUS" + str(toAdd))
        project.tags.add(*toAdd)

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

