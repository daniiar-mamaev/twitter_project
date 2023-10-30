from rest_framework import serializers

from .models import User, Profile
from .validators import password_validation


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=12)
    short_info = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password", "profile_image", "phone_number", "short_info"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        profile_image = validated_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        if password_validation(validated_data['password']):
            user.set_password(validated_data['password'])
            user.save()
        else:
            raise Exception('Enter correct password')
        try:
            profile = Profile.objects.create(
                user=user,
                phone_number=validated_data['phone_number'],
                short_info=validated_data['short_info']
            )
        except Exception as e:
            user.delete()
            raise e
        else:
            profile.username = user.username
            profile.profile_image = user.profile_image
        return profile
