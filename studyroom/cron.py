from .models import Reserve
from datetime import datetime, timedelta

def schedule_monday():
    real_time = datetime.datetime.now().weekday()
    q = Reserve.objects.all()
    q.delete()