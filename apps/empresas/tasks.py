from config import celery_app



@celery_app.task()
def look_for_update():
    return