from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task('cron', id='default', day_of_week='fri', hour='21', minute='00')
def default():
    pass
