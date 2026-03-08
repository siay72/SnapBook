from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer
from rest_framework import serializers
from users.models import User
from decouple import config


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'location',  'phone_number',]


class UserSerializer(BaseUserSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomSerializer"
        fields = ['id', 'email', 'first_name', 'last_name', 'location', 'phone_number', 'profile_picture']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'location', 'phone_number', 'profile_picture']
        read_only_fields = ['email']

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if instance.profile_picture:
            data["profile_picture"] = instance.profile_picture.url

        return data