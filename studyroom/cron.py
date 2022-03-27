from .models import Reserve
import datetime

def schedule_monday():
    real_time = datetime.datetime.now().weekday()
    if real_time == 6:
        q = Reserve.objects.all()
        q.delete()