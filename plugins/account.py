from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.shortcuts import redirect

from conf import app_base
from core.version import Version

env = {}


def init(plugin_env):
    global env
    env = plugin_env
    return Version([0, 0, 2, "alpha"])


def urls():
    return [
        ["%s/account.status$", "account_status", "account/account_status.template.html"],
        ["%s/account.delete_session/(?P<session_id>[0-9]+)/$", "delete_session", None],
        ["%s/account.change_email$", "change_email", None],
        ["%s/account.change_password", "change_password", None],
        ["%s/account.settings$", "account_settings", "account/settings.template.html"]
    ]


def account_status(rq):
    Session = env["getModel"]("Session")
    try:
        session = Session.objects.get(session_hash=env["sessid"](rq))
        sessions = Session.objects.filter(user=session.user, active=True)
        user = session.user
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}
    except Error:
        return {"error": "error"}

    account_status = {}
    account_status["name"] = user.name
    account_status["login"] = user.cn
    account_status["surname"] = user.surname
    account_status["validity"] = user.validity
    account_status["email"] = user.email
    account_status["active_sessions"] = sessions
    account_status["current_session"] = session

    return account_status


def delete_session(rq, session_id):
    Session = env["getModel"]("Session")

    try:
        session = Session.objects.get(id=session_id)
        session.active = False
        session.save()
    except ObjectDoesNotExist:
        return {"error": "Object does not exist"}
    except Error:
        return {"error": "error"}

    return redirect("/%s/account.status" % app_base)


def account_settings(rq):
    context = {}

    if rq.method == "GET":
        context.update(env["csrf"](rq))

    return context


def change_email(rq):
    if rq.method == "POST":
        Session = env["getModel"]("Session")
        try:
            session = Session.objects.get(session_hash=env["sessid"](rq))
            user = session.user
        except ObjectDoesNotExist:
            return {"error": "Object does not exist"}
        except Error:
            return {"error": "error"}

        user.email = rq.POST.get("email")
        user.save()

    return redirect("/%s/account.settings" % app_base)


def change_password(rq):
    if rq.method == "POST":
        Session = env["getModel"]("Session")
        try:
            session = Session.objects.get(session_hash=env["sessid"](rq))
            user = session.user
        except ObjectDoesNotExist:
            return {"error": "Object does not exist"}
        except Error:
            return {"error": "error"}

        old_password = rq.POST.get("old_password")

        if user.password == old_password:
            user.password = rq.POST.get("new_password")
            user.save()
        else:
            return {"error": "wrong password"}

    return redirect("/%s/account.settings" % app_base)
