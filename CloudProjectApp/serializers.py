from rest_framework import serializers
from . import models



class FileSerializer (serializers.ModelSerializer):
    #id_file = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta :
        model = models.File
        fields = '__all__'

class FileProcessedSerializer (serializers.ModelSerializer):
    #id_file = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta :
        model = models.FileProcessed
        fields = '__all__'