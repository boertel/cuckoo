import requests

from flask import current_app

from cuckoo.config import celery
from cuckoo.version import get_version
from cuckoo.webhook import make_digest


# timeout after 30 seconds
TIMEOUT = 30


@celery.task()
def webhook(job_id, application_id, url, data):
    current_app.logger.info('running webhook task')
    signature = make_digest('{}'.format(data), 'my-key')

    headers = {
        'User-Agent': 'cuckoo {}'.format(get_version()),
        'X-Cuckoo-Signature': signature,
        'X-Cuckoo-Job-Id': job_id,
        'X-Cuckoo-Application-Id': application_id,
    }

    response = requests.post(url, data=data, headers=headers, timeout=TIMEOUT)
    if response.status_code != 200:
        current_app.logger.info('invalid response status code')
