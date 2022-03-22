from .models import Reserve
from datetime import datetime, timedelta

def schedule_everyday():
    q = Reserve.objects.all()
    q.delete()


