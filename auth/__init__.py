from flask import Blueprint

auth = Blueprint("auth", __name__, template_folder="templates")

from . import routes

auth.add_url_rule('/', view_func=routes.index, endpoint="index")
auth.add_url_rule('/login', view_func=routes.login, endpoint="login", methods=['GET', 'POST'])
auth.add_url_rule('/logout', view_func=routes.logout, endpoint="logout")