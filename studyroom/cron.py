from .models import Reserve
from datetime import datetime, timedelta

def schedule_everyday():
    real_time = datetime.datetime.now()
    if real_time.weekday() == 4:
        if real_time.hour == 23:
            if real_time.minute == 48:
                q = Reserve.objects.all()
                q.delete()



