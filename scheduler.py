import time
import code
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url='sqlite:///example.sqlite')

scheduler.start()

alarmId = ["1", "2"]


def testCallback():
    print "testCallback: ", time.time()
    # pass


job = scheduler.add_job(testCallback, 'interval', hours=2,
                        id=alarmId[0], replace_existing=True, name="intervaltest")
job2 = scheduler.add_job(testCallback, 'cron', hour=5, minute=45,
                         end_date='2019-05-08', id=alarmId[1], replace_existing=True, name="crontest")
job3 = scheduler.add_job(testCallback, 'date', run_date='2019-11-17 20:30:0')

# month, day, hour, day_of_week, minute, end_date, second, start_date


# https://github.com/agronholm/apscheduler/blob/master/docs/modules/triggers/cron.rst
# job = scheduler.add_job(testCallback, 'interval', seconds=2)

code.interact(local=locals())

while 1:
    # pass
    time.sleep(1)
    print "time: ", time.time()
    # print scheduler.get_jobs()
    # print job
'''
    [('FIELDS_MAP', {
        'week': < class 'apscheduler.triggers.cron.fields.WeekField' >,
        'second': < class 'apscheduler.triggers.cron.fields.BaseField' >,
        'minute': < class 'apscheduler.triggers.cron.fields.BaseField' >,
        'hour': < class 'apscheduler.triggers.cron.fields.BaseField' >,
        'year': < class 'apscheduler.triggers.cron.fields.BaseField' >,
        'day': < class 'apscheduler.triggers.cron.fields.DayOfMonthField' >,
        'day_of_week': < class 'apscheduler.triggers.cron.fields.DayOfWeekField' >,
        'month': < class 'apscheduler.triggers.cron.fields.MonthField' >
    }),
    ('FIELD_NAMES', ('year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second')),
    ('__abstractmethods__', frozenset([])),
    ('__class__', < class 'apscheduler.triggers.cron.CronTrigger' > ),
    ('__delattr__', < method - wrapper '__delattr__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__doc__', '\n    Triggers when current time matches all specified time constraints,\n    similarly to how the UNIX cron scheduler works.\n\n    :param int|str year: 4-digit year\n    :param int|str month: month (1-12)\n    :param int|str day: day of the (1-31)\n    :param int|str week: ISO week (1-53)\n    :param int|str day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)\n    :param int|str hour: hour (0-23)\n    :param int|str minute: minute (0-59)\n    :param int|str second: second (0-59)\n    :param datetime|str start_date: earliest possible date/time to trigger on (inclusive)\n    :param datetime|str end_date: latest possible date/time to trigger on (inclusive)\n    :param datetime.tzinfo|str timezone: time zone to use for the date/time calculations (defaults\n        to scheduler timezone)\n    :param int|None jitter: advance or delay the job execution by ``jitter`` seconds at most.\n\n    .. note:: The first weekday is always **monday**.\n    '),
    ('__format__', < built - in method __format__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__getattribute__', < method - wrapper '__getattribute__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__getstate__', < bound method CronTrigger.__getstate__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__hash__', < method - wrapper '__hash__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__init__', < bound method CronTrigger.__init__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__module__', 'apscheduler.triggers.cron'),
    ('__new__', < built - in method __new__ of type object at 0x55f5b2b93b80 > ),
    ('__reduce__', < built - in method __reduce__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__reduce_ex__', < built - in method __reduce_ex__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__repr__', < bound method CronTrigger.__repr__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__setattr__', < method - wrapper '__setattr__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__setstate__', < bound method CronTrigger.__setstate__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__sizeof__', < built - in method __sizeof__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__slots__', ('timezone', 'start_date', 'end_date', 'fields', 'jitter')),
    ('__str__', < bound method CronTrigger.__str__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__subclasshook__', < built - in method __subclasshook__ of ABCMeta object at 0x55f5b427b030 > ),
    ('_abc_cache', < _weakrefset.WeakSet object at 0x7fe633b08910 > ),
    ('_abc_negative_cache', < _weakrefset.WeakSet object at 0x7fe633b08ad0 > ),
    ('_abc_negative_cache_version', 29),
    ('_abc_registry', < _weakrefset.WeakSet object at 0x7fe633b08a50 > ),
    ('_apply_jitter', < bound method CronTrigger._apply_jitter of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('_increment_field_value', < bound method CronTrigger._increment_field_value of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('_set_field_value', < bound method CronTrigger._set_field_value of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('end_date', datetime.datetime(2019, 5, 8, 0, 0, tzinfo = < DstTzInfo 'America/Vancouver')









    ('FIELD_NAMES', ('year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second')),
    ('__class__', < class 'apscheduler.triggers.cron.CronTrigger' > ),
    ('__getattribute__', < method - wrapper '__getattribute__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__getstate__', < bound method CronTrigger.__getstate__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__hash__', < method - wrapper '__hash__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__init__', < bound method CronTrigger.__init__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__module__', 'apscheduler.triggers.cron'),
    ('__reduce__', < built - in method __reduce__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__reduce_ex__', < built - in method __reduce_ex__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__repr__', < bound method CronTrigger.__repr__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__setattr__', < method - wrapper '__setattr__' of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__setstate__', < bound method CronTrigger.__setstate__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__sizeof__', < built - in method __sizeof__ of CronTrigger object at 0x7fe633ba27e0 > ),
    ('__slots__', ('timezone', 'start_date', 'end_date', 'fields', 'jitter')),
    ('__str__', < bound method CronTrigger.__str__ of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('__subclasshook__', < built - in method __subclasshook__ of ABCMeta object at 0x55f5b427b030 > ),
    ('_abc_cache', < _weakrefset.WeakSet object at 0x7fe633b08910 > ),
    ('_abc_negative_cache', < _weakrefset.WeakSet object at 0x7fe633b08ad0 > ),
    ('_abc_negative_cache_version', 29),
    ('_abc_registry', < _weakrefset.WeakSet object at 0x7fe633b08a50 > ),
    ('_apply_jitter', < bound method CronTrigger._apply_jitter of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),
    ('_set_field_value', < bound method CronTrigger._set_field_value of < CronTrigger(hour = '5', minute = '45', end_date = '2019-05-08 00:00:00 PDT', timezone = 'America/Vancouver') >> ),



'''
