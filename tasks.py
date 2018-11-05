import time
import traceback
import uwsgi
from uwsgidecorators import thread, spool
# from uwsgi_tasks import task, TaskExecutor


def threaded_task(duration):
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(1)


@thread
def uwsgi_task(duration):
    for i in range(duration):
        print("Working in uwsgi thread... {}/{}".format(i + 1, duration))
        time.sleep(1)


@spool
def spool_task(args):
    try:
        duration = int(args['duration'])
        for i in range(duration):
            print("Working in uwsgi spool... {}/{}".format(i + 1, duration))
            time.sleep(1)
        return uwsgi.SPOOL_OK
    except Exception as e:
        print(traceback.format_exc())
        return uwsgi.SPOOL_RETRY


# @task(executor=TaskExecutor.SPOOLER)
# def uwsgi_tasks_task(duration):
#     for i in range(duration):
#         print("Working in uwsgi-tasks spool... {}/{}".format(i + 1, duration))
#         time.sleep(1)
