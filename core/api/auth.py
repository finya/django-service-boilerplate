from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.compat import authenticate

from core.api.inspectors import StandardizedAutoSchema


class AuthTokenSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class StandardizedObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    schema = StandardizedAutoSchema()


OBTAIN_AUTH_TOKEN = StandardizedObtainAuthToken.as_view()
