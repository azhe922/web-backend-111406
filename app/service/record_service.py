from app.model.record import Record
from app.model.user import User
from app.enums.training_part import TrainingPart
from datetime import date, datetime as dt
from statistics import fmean

def search_records_by_userid(user_id):
    records = Record.objects(user_id=user_id).order_by('-create_time')
    return [record.to_json() for record in records]

def get_count(user_id):
    return len(Record.objects(user_id=user_id))

def get_biceps_means():
    biceps_records = Record.objects(part=TrainingPart.biceps).aggregate(*[
        {
            '$group': {
                '_id': "$user_id",
                'times': { '$avg': '$times' }
            }
        }, {
                '$lookup': {
                'from': User._get_collection_name(),
                'localField': '_id',
                'foreignField': 'user_id',
                'as': 'relation'}
        }
    ])
    biceps_results = __format_result(biceps_records)
    statistics_results = []
    __append_statistics(biceps_results, statistics_results)
    return statistics_results


def get_quadriceps_means():    
    quadriceps_records = Record.objects(part=TrainingPart.quadriceps).aggregate(*[
        {
            '$group': {
                '_id': "$user_id",
                'times': { '$avg': '$times' }
            }
        }, {
                '$lookup': {
                'from': User._get_collection_name(),
                'localField': '_id',
                'foreignField': 'user_id',
                'as': 'relation'}
        }
    ])
    
    quadriceps_results = __format_result(quadriceps_records)

    statistics_results = []
    __append_statistics(quadriceps_results, statistics_results)
    return statistics_results


def __get_age(birthdate: date):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def __sort_by_age(result):
    return result.get('age')

def __format_result(records):
    results = []
    for r in records:
        birthday_str = r['relation'][0]['birthday']
        birthday = dt.strptime(birthday_str, '%Y%m%d').date()
        result = {
            'user_id': r['_id'],
            'times': round(r['times']),
            'age': __get_age(birthday)
        }
        results.append(result)
    results.sort(key=__sort_by_age)
    return results

def __append_statistics(biceps_results, statistics_results):
    for minage in range(60, 100, 5):
        maxage = minage + 5
        interval = []
        for br in biceps_results:
            age = br.get('age')
            if age >= minage and age < maxage:
                interval.append(br.get('times'))
            if age >= maxage:
                break
        statistics_results.append(round(fmean(interval))) if interval else statistics_results.append(0)