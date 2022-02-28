from .models import Reserve, Result
import datetime

def schedule_every_ten_minutes():
    today = datetime.datetime.now()
    day_standard = datetime.datetime(2022, 3, 1, 0, 0, 0)
    diff_hours = datetime.timedelta(hours=10)
    result = Result.objects.filter(semester='2022-2')
    for a in result:
        result = a

    random_result = Result.objects.filter(semester='2022-2')
    for random in random_result:
        random_result = random
    random_result_list = random_result.sequence.split(',')

    if today > day_standard is True:
        if today < day_standard + diff_hours is True:
            random_result_list.reverse()
            a = random_result_list.pop()
            random_result_list.reverse()
            list = ','.join(random_result_list)

            result.current = a
            result.sequence = list
            result.save()