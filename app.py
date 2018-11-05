import os
import time
from flask import Flask, jsonify
from threading import Thread
from tasks import threaded_task, uwsgi_task, spool_task # , uwsgi_tasks_task

app = Flask(__name__)
app.secret_key = os.urandom(42)


@app.route("/", defaults={'duration': 5})
@app.route("/<int:duration>")
def index(duration):
    thread = Thread(target=threaded_task, args=(duration,))
    thread.daemon = True
    thread.start()
    return jsonify({'thread_name': str(thread.name),
                    'started': True})


@app.route("/uwsgi_thread", defaults={'duration': 5})
@app.route("/uwsgi_thread/<int:duration>")
def uwsgi_thread(duration):
    uwsgi_task(duration)
    return jsonify({'started': True})


def prepare_spooler_args(**kwargs):  # maybe spool(pass_arguments=True)
    args = {}
    for name, value in kwargs.items():
        args[name.encode('utf-8')] = str(value).encode('utf-8')
    return args


@app.route("/uwsgi_spool", defaults={'duration': 5})
@app.route("/uwsgi_spool/<int:duration>")
def uwsgi_spool(duration):
    ### #  at = int(time.time()) + duration
    args = prepare_spooler_args(duration=duration)
    spool_task.spool(args)
    return jsonify({'started': True})


@app.route("/uwsgi_tasks", defaults={'duration': 5})
@app.route("/uwsgi_tasks/<int:duration>")
def uwsgi_tasks(duration):
    # https://pypi.org/project/uwsgi-tasks/
    # hot to pass at param?
    uwsgi_tasks_task(duration)
    return jsonify({'started': True})


if __name__ == '__main__':
    app.run(debug=True)
