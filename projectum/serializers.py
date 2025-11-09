from rest_framework import serializers
from .models import *

"""USER SERIALIZERS"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "date_joined",
            "is_staff",
        ]

        read_only_fields = ["id", "date_joined", "is_staff"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


"""PROJECT SERIALIZERS"""


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    collaborators = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "status",
            "tags",
            "author",
            "collaborators",
            "thumbnail",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at", "author"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        project = Project.objects.create(**validated_data)

        for tag in tags_data:
            tag_obj, _ = Tag.objects.get_or_create(name=tag["name"])
            project.tags.add(tag_obj)

        return project
