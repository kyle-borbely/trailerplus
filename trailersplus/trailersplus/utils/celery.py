from time import sleep
from datetime import datetime as dt


def wait_for_result(task, timeout=60, idle=3):
    start_time = dt.now()
    while end_time := (dt.now() - start_time).seconds < timeout:
        if task.status != 'SUCCESS':
            sleep(idle)
            end_time = dt.now()
            continue
        else:
            return task
    raise ConnectionError('Can not recieve result')
