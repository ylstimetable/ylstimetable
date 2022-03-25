from .models import Reserve
from datetime import datetime, timedelta

def schedule_everyday():
    real_time = datetime.datetime.now().weekday()
    if real_time == 5:
        q = Reserve.objects.all()
        q.delete()



