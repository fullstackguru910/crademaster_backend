from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import IDFile

User = get_user_model()

class ReferredUserSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'date_joined', 'earning']

    def get_earning(self, obj):
        return 0


class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDFile
        fields = ('id', 'front', 'back')
