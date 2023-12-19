from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
