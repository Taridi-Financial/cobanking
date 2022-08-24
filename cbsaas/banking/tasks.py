from config import celery_app
from time import sleep


@celery_app.task()
def celery_test_print():
    sleep(30)
    print('mot na kokufa')
   