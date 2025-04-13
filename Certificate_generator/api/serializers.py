from rest_framework import serializers

class CertificateRequestSerializer(serializers.Serializer):
    template = serializers.FileField()
    csvfile = serializers.FileField()
    sender_email = serializers.EmailField()
    sender_password = serializers.CharField()
