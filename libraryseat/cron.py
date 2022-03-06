from .models import Reserve, Result
import datetime

def schedule_every_ten_minutes():
    today = datetime.datetime.now()
    day_standard = datetime.datetime(2022, 3, 6, 8, 0, 0)
    diff_hours = datetime.timedelta(hours=10)
    day_standard_ten_hours = day_standard+diff_hours
    day_standard_twenty_hours = day_standard_ten_hours+diff_hours
    result = Result.objects.filter(semester='2022-2')
    for a in result:
        result = a

    random_result = Result.objects.filter(semester='2022-2')
    for random in random_result:
        random_result = random
    random_result_list = random_result.sequence.split(',')

    if today > day_standard:
        if today.hour >= day_standard_ten_hours.hour:
            if today.hour < day_standard_twenty_hours.hour:
                random_result_list.reverse()
                a = random_result_list.pop()
                random_result_list.reverse()
                list = ','.join(random_result_list)

                result.current = a
                result.sequence = list
                result.save()
