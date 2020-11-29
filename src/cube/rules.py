from datetime import datetime, timedelta 
from django.db.models import Count, Sum
from background_task import background
import requests
from . import models
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Trigger(object):

    @background(schedule=timedelta(seconds=5))
    def notify_user(user_id=None, event_id=None):

        print("Checking {} and {}".format(user_id, event_id))
        user = models.User.objects.get(pk=user_id)
        event = models.Event.objects.get(pk=event_id)

        ts_before = datetime.strptime(event.ts, "%Y%m%d %H%M%S")
        ts_curr = (ts_before + timedelta(minutes=15)).strftime("%Y%m%d %H%M%S")

        fdbk_event = models.Event.objects\
            .filter(ts__range=[event.ts, ts_curr])\
            .filter(userid=user)\
            .filter(marked=False)\
            .filter(noun='fdbk')\
            .first()
        if not fdbk_event:
            try:
                # call Dummy API to alert operator
                response = requests.post(url="http://" + get_ip() + ":8000/api/v1/dummyapi", data={"message": "Didn't recieve feedback for user {} and  event {}".format(user_id, event_id)})
                print(response)
            except Exception as exe:
                print(exe)
        else:
            fdbk_event.marked = True
            fdbk_event.save()

class Rules(object):
    def _first_bill_pay(self, user=None, event=None):    
        if user and event:
            if event.noun == 'bill':
                bill_events = user.event_set.filter(noun="bill").all()
                if (bill_events) and (len(bill_events) == 1) and (event in bill_events):
                    return True, "First Bill Pay by user {}".format(user.userid)
                return False, "NR"
            return False, "NR"     
        return False, "NR"

    def _frequent_payment(self, user=None, event=None):
        if user and event:

            if event.verb == 'pay' and event.noun == 'bill':
                
                # Timestamps in datetime format
                ts_curr = datetime.strptime(event.ts, "%Y%m%d %H%M%S")
                ts_before = (ts_curr - timedelta(minutes=5)).strftime("%Y%m%d %H%M%S")

                # Filter all events based on timestamp and noun
                eve = user.event_set.filter(noun="bill").filter(ts__range=[ts_before, event.ts])
                
                # Groups on noun and returns count and sum of values
                result = eve.values("noun").annotate(count=Count('payment__value'), sum=Sum("payment__value"))
                if result and result[0]["count"] >= 5 and result[0]["sum"] >= 20000:
                    return True, "Alert user of frequent events"
                else:
                    return False, "NR"
            else:
                return False, "NR"
        return False, "NR"
    
    def implement_rules(self, user=None, event=None, request=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        print(IP)
        if user and event and request:
            global base_url
            base_url = request.scheme + '://' + request.get_host() + '/api/v1/dummyapi'

            res, message = self._first_bill_pay(user, event)
            if res:
                response = requests.post(base_url, data={"message": message})

            res, message = self._frequent_payment(user, event)
            if res:
                response = requests.post(base_url, data={"message": message})

            Trigger().notify_user(user_id=user.userid, event_id=event.id)

            return True
        else:
            return False
