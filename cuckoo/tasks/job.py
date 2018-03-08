from flask import current_app

from cuckoo.config import celery


@celery.task()
def job():
    current_app.logger.info('running job task')
