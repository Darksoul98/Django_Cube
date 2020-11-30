import logging

from django.shortcuts import render
from request_log.mixins import RequestLogViewMixin
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers
from .rules import Rules

logger = logging.getLogger(__name__)

class EventsAPI(generics.GenericAPIView):

    serializer_class = serializers.EventSerializer

    def post(self, request):
        try:
            # For the assignment purpose only, as current DB will have 0 users
            # This Creates one if doesn't exist
            user = models.User.objects.filter(userid=request.data["userid"]).first()
            if not isinstance(user, models.User):
                user = models.User(
                    userid=request.data["userid"]
                )
                user.save()
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                user = models.User.objects.filter(userid=data["userid"]).first()
                if not isinstance(user, models.User):
                    return Response({"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

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
                
                # Call to Rules library
                rules = Rules().implement_rules(user, event, request)

                return Response({"message": "Saved Event " + str(event.id)}, status=status.HTTP_200_OK)

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
