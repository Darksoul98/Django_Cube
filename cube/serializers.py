from rest_framework import exceptions, serializers, status
from . import models
# class PaymentSerializer(serializers.Serializer):
class PaymentSerializer(serializers.ModelSerializer):
    # bank = serializers.CharField(required=True)
    # merchantid = serializers.IntegerField(required=True)
    # value = serializers.IntegerField(required=True)
    # mode = serializers.CharField(required=True)

    class Meta:
        model = models.Payment
        fields = [
            'bank',
            'merchantid',
            'value',
            'mode',
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    # text = serializers.CharField(required=True)

    class Meta:
        model = models.Feedback
        fields = [
            'text',
        ]

class EventSerializer(serializers.ModelSerializer):
    # prop = serializers.SerializerMethodField() #(source='properties')
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
            # 'prop',
            'properties',
        ]
    
    # def get_prop(self, obj):
    #     import pdb; pdb.set_trace()
    #     if obj["noun"] == "bill":
    #         return PaymentSerializer(obj["properties"]).data
    #     elif obj["noun"] == "fdbk":
    #         return FeedbackSerializer(obj["properties"]).data
    #     else:
    #         raise Exception("Invalid Noun")