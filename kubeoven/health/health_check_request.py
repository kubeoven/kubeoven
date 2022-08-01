import backoff
import requests
import logging

@backoff.on_exception(backoff.expo, Exception, max_tries=10)
def health_check_request(url: str, component):
    logging.getLogger('backoff').setLevel(logging.FATAL)
    res = requests.get(url, verify=False)
    if not res.ok:
        raise RuntimeError(f'{component} is unhealthy')

