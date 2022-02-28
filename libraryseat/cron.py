from .models import Reserve, Result
from datetime import datetime, timedelta

def schedule_every_ten_minutes():

    today = datetime.now()
    day_standard = datetime.date(2022, 3, 2, 10, 0, 0)
    diff_hours = timedelta(hours=10)
    result = Result.objects.filter(semester='2022-2')
    for a in result:
        result = a

    reserve_all = Reserve.objects.all()
    random_result = Result.objects.fitler(semester='2022-2')
    for random in random_result:
        random_result = random
    random_result_list = random_result.split(',')

    if today > day_standard is True:
        if today < day_standard+diff_hours is True:
            random_result_list.reverse()
            a = random_result_list.pop()
            random_result_list.reverse()
            list = ','.join(random_result_list)

            result.current = a
            result.sequence = list
            result.save()

