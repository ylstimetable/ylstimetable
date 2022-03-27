from .models import Reserve
from datetime import datetime, timedelta


def schedule_weekday():
    real_time = datetime.datetime.now().weekday()
    if real_time == 6:
        q = Reserve.objects.all()
        q.delete()
