from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from . import models, serializers
from .rules import Rules
from request_log.mixins import RequestLogViewMixin

import logging
logger = logging.getLogger(__name__)

class EventsAPI(generics.GenericAPIView):
    '''
        {"noun": "bill", "userid": 178765, "ts": "20170315 134850", "latlong": "19.07,72.87", "verb": "pay", "timespent": 72, "properties": {"bank": "hdfc", "merchantid": 234, "value": 139.5, "mode": "netbank"}}
        
        {"noun": "fdbk", "userid": 178765, "ts": "20170315 145250", "latlong": "19.07,72.87", "verb": "post", "timespent": null, "properties": {"text": "the bank page took too long to load"}}
    '''
    serializer_class = serializers.EventSerializer

    def post(self, request):
        try:
            # import pdb; pdb.set_trace()
            # user = models.User.objects.filter(userid=request.data["userid"]).first()
            # if not isinstance(user, models.User):
            #     user = models.User(
            #         userid=request.data["userid"]
            #     )
            #     user.save()
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = models.User.objects.filter(userid=data["userid"]).first()
                if not isinstance(user, models.User):
                    return Response({"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
                # del data["userid"]
                # Creating Event 
                event = models.Event(
                    userid=user, 
                    ts=data["ts"],
                    latlong=data["latlong"],
                    noun=data["noun"],
                    verb=data["verb"],
                    timespent=data["timespent"])
                event.save()
                
                # If noun = bill and verb = pay Create Payment
                if event.noun == "bill" and event.verb == "pay":
                    payment = serializers.PaymentSerializer(data=data["properties"])
                    if payment.is_valid():
                        new_payment = models.Payment(eventid=event, **payment.data)
                        new_payment.save()
                    else:
                        return Response({"message": payment.errors}, status=status.HTTP_400_BAD_REQUEST)

                    # If noun = fdbk and verb = post Create Feedback
                elif event.noun == "fdbk" and event.verb == "post":
                    feedback = serializers.FeedbackSerializer(data=data["properties"])
                    if feedback.is_valid():
                        new_feedback = models.Feedback(eventid=event, **feedback.data)
                        new_feedback.save()
                    else:
                        return Response({"message": feedback.errors}, status=status.HTTP_400_BAD_REQUEST)
                
                rules = Rules().implement_rules(user, event, request)
                # # Call Rules on event
                # res, message = Rules().first_bill_pay(user, event)
                # if res:
                #     print(message)
                
                # res, message = Rules().frequent_payment(user, event)
                # if res:
                #     print(message)

                return Response({"message": "noted"}, status=status.HTTP_200_OK)

            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            print(exe)
            return Response({"message": str(exe)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DummyAPI(RequestLogViewMixin, generics.GenericAPIView):

    def post(self, request):
        try:
            return Response({"message": "Trigger Sent"}, status=status.HTTP_200_OK)
        except Exception as exe:
            return Response({"message": str(exe)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
