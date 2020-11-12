from flask import Blueprint, g
from flask_login import login_required, current_user

private = Blueprint("private", __name__, template_folder="templates", url_prefix="/private")


@private.before_request
@login_required
def do_login():
    g.user = current_user

from . import routes

private.add_url_rule('/', view_func=routes.index, endpoint="index")
private.add_url_rule('/test', view_func=routes.test_task, endpoint="test_task")
private.add_url_rule('/single-task', view_func=routes.single_task_view, endpoint="single_task", methods=['GET', 'POST'])
private.add_url_rule('/subtasks', view_func=routes.sub_tasks, endpoint="subtasks", methods=['GET', 'POST'])
private.add_url_rule('/one-at-a-time', view_func=routes.sub_tasks, endpoint="one_at_a_time", methods=['GET', 'POST'])

