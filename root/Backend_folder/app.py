from application import create_app
from application.worker import celery_init_app

app = create_app()
celery_app = celery_init_app(app)

from application.modules.tasks import sendDailyReminder, sendMonthlyReport, removeReports
from celery.schedules import crontab
#configure scheduled tasks
# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(crontab(minute='1', hour='9', day_of_month='28'),
#                             sendMonthlyReport.s()
#                              )
    
#     sender.add_periodic_task(crontab(minute='25', hour='2'),
#                             sendDailyReminder.s()
#                              )

#     sender.add_periodic_task(crontab(minute='30', hour='5', day_of_week='1'),
#                             removeReports.s()
#                              )

if __name__ == "__main__":
    app.run()