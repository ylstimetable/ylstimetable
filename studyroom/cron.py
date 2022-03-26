from .models import Reserve
from datetime import datetime, timedelta

def schedule_week():
    q = Reserve.objects.all()
    q.delete()
