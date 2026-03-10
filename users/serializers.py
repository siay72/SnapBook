from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer
from rest_framework import serializers
from decouple import config
from djoser.serializers import TokenCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'location',  'phone_number',]


class UserSerializer(BaseUserSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomSerializer"
        fields = ['id', 'email', 'first_name', 'last_name', 'location', 'phone_number', 'profile_picture',"is_staff",]

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
    


class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        refresh = RefreshToken.for_user(self.user)

        data["access"] = str(refresh.access_token)

        data["access_token"] = {
            "user_id": self.user.id,
            "is_staff": self.user.is_staff,
        }

        return data