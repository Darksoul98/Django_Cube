from datetime import datetime, timedelta 
from django.db.models import F, Count, Sum
from background_task import background
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
class Trigger(object):

    @background(schedule=timedelta(seconds=1))
    def notify_user(user_id=None):
        logger.error('Notified usawdwaer ' + str(user_id))

class Rules(object):
    def _first_bill_pay(self, user=None, event=None):    
        if user and event:
            if event.noun != 'bill':
                no_events = user.event_set.filter(noun="bill").all()
                if (no_events) and (len(no_events) == 1) and (event in no_events):
                    return True, "First Bill Pay"
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
    
    def implement_rules(self, user=None, event=None):
        if user and event:
            res, message = self._first_bill_pay(user, event)
            print(message)
            res, message = self._frequent_payment(user, event)
            print(message)

            logger.error('Notified user' + str(user.userid))

            Trigger().notify_user(user_id=user.userid)

            return True
        else:
            return False
