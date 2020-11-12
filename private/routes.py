from flask import request, render_template
from tasks import single_task, parent_task, one_at_a_time, test


def index():
    return render_template("private/layout.html")


def test_task():
    test.send()
    return render_template("private/test.html")


def single_task_view():
    if request.method == "POST":
        name = request.form.get("name", "-")
        duration = int(request.form.get("duration", 1))
        single_task.send(name, duration)

    return render_template("private/single_task.html")


def sub_tasks():
    if request.method == "POST":
        name = request.form.get("name", "-")
        n_subtasks = int(request.form.get("subtasks", 1))
        parent_task.send(name, n_subtasks)

    return render_template("private/sub_tasks.html")


def one_at_a_time_view():
    name = request.args.get('name', 'asdf')
    one_at_a_time.send(name)
    return f"OK {name}"
