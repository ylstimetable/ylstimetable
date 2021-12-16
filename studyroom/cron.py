from .models import Reserve
from datetime import datetime, timedelta

def schedule_everyday():
    today = datetime.now()
    diff_days = timedelta(days=1)
    yesterday = today - diff_days
    q = Reserve.objects.filter(year=yesterday.year, month=yesterday.month, day=yesterday.day)
    q.delete()
