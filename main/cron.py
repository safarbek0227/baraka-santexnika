from .models import MontylyReport

def my_cron_job():
    MontylyReport.objects.create(income=0, outcome=0, stock=0, sells=0)
    print('hello')