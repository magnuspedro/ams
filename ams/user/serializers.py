from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from core.models import Modality, User

from modality.serializers import ModalitySerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    modalities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modality.objects.all()
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'cpf', 'rg', 'course', 'phone',
                  'sex', 'date_of_birth', 'modalities')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        modalities = validated_data.pop('modalities')
        user = get_user_model().objects.create_user(**validated_data)
        for modality in modalities:
            user.modalities.add(modality)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(UserSerializer):
    modalities = ModalitySerializer(many=True, read_only=True)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        else:
            is_staff = User.objects.values('is_staff').get(email=email)

            if not is_staff['is_staff']:
                msg = _('Unable to authenticate with provided credentials')
                raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
