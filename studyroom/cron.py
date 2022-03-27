from .models import Reserve
import datetime

def schedule_monday():
    real_time = datetime.datetime.now().weekday()
    q = Reserve.objects.all()
    q.delete()