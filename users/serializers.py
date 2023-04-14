from rest_framework import  serializers
from .models import User, UserConfirmation


class SignUpSerializer(serializers.ModelSerializer):
    guid  = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "guid",
            "auth_type",
            "auth_status"
        )
        extra_kwargs = {
            "auth_type": {'read_only': True, 'required':False},
            "auth_status": {'read_only':True, 'required':False}
        }



        





