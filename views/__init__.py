from flask import Blueprint, request, escape, render_template
from tasks import test, single_task as st, parent_task


views = Blueprint("views", __name__, template_folder="templates")


@views.route("/")
def index():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@views.route('/test')
def test_task():
    test.send()
    return 'Test task sended to dramatiq'


@views.route('/single-task', methods=["GET", "POST"])
def single_task():
    if request.method == "POST":
        name = request.form.get("name", "-")
        duration = int(request.form.get("duration", 1))
        st.send(name, duration)

    return render_template("views/single_task.html")


@views.route('/sub-tasks', methods=["GET", "POST"])
def sub_tasks():
    if request.method == "POST":
        name = request.form.get("name", "-")
        n_subtasks = int(request.form.get("subtasks", 1))
        parent_task.send(name, n_subtasks)

    return render_template("views/sub_tasks.html")
