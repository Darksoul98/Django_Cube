from rest_framework import serializers
from . import models

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Payment
        fields = [
            'bank',
            'merchantid',
            'value',
            'mode',
        ]

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Feedback
        fields = [
            'text',
        ]

class EventSerializer(serializers.ModelSerializer):
    properties = serializers.JSONField()

    class Meta:
        model = models.Event
        fields = [
            'noun',
            'userid',
            'ts',
            'latlong',
            'verb',
            'timespent',
            'properties',
        ]
