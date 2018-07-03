from rest_framework import serializers

from apps.v1.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """
    This class is handles all the necessary logic for User Model. And  It should not be used as it.
    It should be inherited and add fields you need for you serializer.
    Since this class contain all the fields it may be vulnerable
    """
    token = serializers.ReadOnlyField(source='auth_token.key')
    user_id = serializers.ReadOnlyField(source='id')
    password_again = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'token',
            'username',
            'email',
            'password',
            'password_again',
            'is_active',
            'is_superuser',
            'is_staff',
            'date_joined',
            'last_login',
        ]
        extra_kwargs = {'password':{'write_only':True}}
        read_only_fields = ['user_id', 'token', 'is_active', 'date_joined', 'last_login', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        password_again = attrs.get('password_again')
        if password != password_again:
            raise serializers.ValidationError('Password and Password Again does not match')
        return attrs


class DynamicFieldSerializerMixin:
    class LPMeta:
        fields = []
        exclude = []

    def get_lp_fields(self):
        self.lp_fields = getattr(self.LPMeta, 'fields', None)
        self.lp_exclude = getattr(self.LPMeta, 'exclude', None)

        assert not (self.lp_fields and self.lp_exclude), (
            "Cannot set both 'fields' and 'exclude' options on "
            "serializer {serializer_class}.".format(
                serializer_class=self.__class__.__name__
            )
        )

        assert not (self.lp_fields is None and self.lp_exclude is None), (
            "Creating a without either the 'fields' or 'exclude attribute "
            "{serializer_class} serializer is not allowed.".format(
                serializer_class=self.__class__.__name__
            ),
        )

    def get_fields(self):
        fields = super().get_fields()
        self.get_lp_fields()
        if self.lp_fields is not None:
            for field in list(fields.keys()):
                if field not in self.lp_fields:
                    fields.pop(field)
        if self.lp_exclude is not None:
            for ex in self.lp_exclude:
                fields.pop(ex)
        return fields


class UserSerializer(DynamicFieldSerializerMixin, BaseUserSerializer):
    class LPMeta:
        exclude = ['password', 'password_again']


class UserSignupSerializer(DynamicFieldSerializerMixin, BaseUserSerializer):
    class LPMeta:
        fields = ['email', 'username', 'password', 'password_again', 'token', 'user_id']
