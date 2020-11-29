from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"
    userid = models.IntegerField(primary_key=True)


class Event(models.Model):
    class Meta:
        db_table = "event"
    userid = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ts = models.CharField(max_length=255, null=False, blank=False)  # timestamp Field
    latlong = models.CharField(max_length=255)
    noun = models.CharField(max_length=10)
    verb = models.CharField(max_length=10)
    timespent = models.IntegerField(null=True, blank=False)  # timespent on screen
    marked = models.BooleanField(null=False, default=False)

class Payment(models.Model):
    class Meta:
        db_table = "payment"
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
    bank = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    merchantid = models.IntegerField(null=False, blank=False, default=0)
    value = models.FloatField(null=False, blank=False, default=0)

class Feedback(models.Model):
    class Meta:
        db_table = "feedback"
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
