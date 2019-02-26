from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import CharField, EmailField, ValidationError
from rest_framework.validators import UniqueValidator
from django.db.models import Q



class UserSerializer(serializers.ModelSerializer):
    phonenum = serializers.CharField(source='profile.phonenum')
    city = serializers.CharField(source='profile.city')
    gender = serializers.CharField(source='profile.gender')
    dob = serializers.CharField(source='profile.dob')

    class Meta:
        model = User
        depth = 1
        fields = ('id', 'username', 'email', 'phonenum', 'city', 'gender', 'dob')

    def update(self, instance, validated_data):
        # retrieve the Profile
        profile_data = validated_data.pop('profile', None)

        for attr, value in profile_data.items():
            setattr(instance.profile, attr, value)

        # retrieve User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.profile.save()
        instance.save()
        return instance


#
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


#
class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token')

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not email and not username:
            raise ValidationError("username or email is required to login")

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("username or email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("incorrect credentials, try again.")
        # token = Token.objects.get(user=user_obj)
        data["token"] = "data"

        return data
