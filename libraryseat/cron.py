from .models import Reserve, Result, Receipt
import datetime

def schedule_every_ten_minutes():
    result_count = len(Result.objects.filter(semester='2023-1'))

    if result_count != 0:
        result = Result.objects.filter(semester='2023-1')
        for a in result:
            result = a
        receipt = Receipt.objects.filter(semester='2023-1')
        for a in receipt:
            receipt = a

        today = datetime.datetime.now()
        day_standard = datetime.datetime(2023, int(receipt.month), int(receipt.day), 0, 0, 0)
        diff_hours = datetime.timedelta(hours=9)
        day_standard_nine_hours = day_standard + diff_hours
        day_standard_twentythree_hours = day_standard_nine_hours + diff_hours + datetime.timedelta(hours=5)

        random_result = Result.objects.filter(semester='2023-1')
        for random in random_result:
            random_result = random
        random_result_list = random_result.sequence.split(',')

        if today > day_standard:
            if today.hour >= day_standard_nine_hours.hour:
                if today.hour < day_standard_twentythree_hours.hour:
                    random_result_list.reverse()
                    a = random_result_list.pop()
                    random_result_list.reverse()
                    list = ','.join(random_result_list)

                    result.current = a
                    result.sequence = list
                    result.save()
                   
    else:
        result = Result.objects.filter(semester='2000-0')
        for a in result:
            result = a
            
        result.current = 'UPDATING'
