from flask import redirect, url_for, request, render_template, flash
from flask_login import login_user, login_required, current_user
from models import User


def index():
    return redirect(url_for('auth.login'))


def login():
    if request.method == "POST":
        name = request.form.get("name")
        account = request.form.get("account")
        if not name.strip():
            flash("Empty name", "error")

        user = User()
        user.name = name
        user.account = account
        User.save(user)

        login_user(user)

        return redirect(url_for("private.index"))
    else:
        return render_template("auth/login.html")


@login_required
def logout():
    User.delete(current_user)
    return redirect(url_for('auth.index'))