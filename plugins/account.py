from django.shortcuts import redirect

from conf import app_base
from core.version import Version

env = {}


def init(plugin_env):
    global env
    env = plugin_env
    return Version([0, 1, 0, "alpha"])


def urls():
    return [
        ["%s/account.status$", "account_status", "account/account_status.template.html"],
        ["%s/account.delete_session/(?P<session_id>[0-9]+)/$", "delete_session", None],
        ["%s/account.change_email$", "change_email", None],
		["%s/account.rfid_state$", "rfid_state", None],
        ["%s/account.change_password$", "change_password", None],
        ["%s/account.settings", "account_settings", "account/settings.template.html"]
    ]


def account_status(rq):
    Session = env["getModel"]("Session")
    try:
        current_session = Session.objects.get(session_hash=env["sessid"](rq))
        sessions = Session.objects.filter(user=current_session.user, active=True)
    except Exception as e:
            return redirect("/%s/account.settings?error=%s" % (app_base, str(e)))

    return {"active_sessions": sessions, "current_session": current_session}


def delete_session(rq, session_id):
    Session = env["getModel"]("Session")

    try:
        session = Session.objects.get(id=session_id)
        session.active = False
        session.save()
    except Exception as e:
            return redirect("/%s/account.settings?error=%s" % (app_base, str(e)))

    return redirect("/%s/account.status?msg=Session closed" % app_base)


def account_settings(rq):
    context = {"msg": rq.GET.get("msg"), "error": rq.GET.get("error")}

    if rq.method == "GET":
        context.update(env["csrf"](rq))
    return context


def change_email(rq):
    if rq.method == "POST":
        Session = env["getModel"]("Session")
        try:
            session = Session.objects.get(session_hash=env["sessid"](rq))
            user = session.user
        except Exception as e:
            return redirect("/%s/account.settings?error=%s" % (app_base, str(e)))

        user.email = rq.POST.get("email")
        user.save()
        return redirect("/%s/account.settings?msg=Email changed" % app_base)
    return redirect("/%s/account.settings?error=Invalid request" % app_base)


def change_password(rq):
    if rq.method == "POST":
        Session = env["getModel"]("Session")
        try:
            session = Session.objects.get(session_hash=env["sessid"](rq))
            user = session.user
        except Exception as e:
            return redirect("/%s/account.settings?error=%s" % (app_base, str(e)))

        old_password = rq.POST.get("old_password")

        if user.password == old_password:
            user.password = rq.POST.get("new_password")
            user.save()
        else:
            return redirect("/%s/account.settings?error=Invalid password" % app_base)

    return redirect("/%s/account.settings?msg=Password updated" % app_base)
	
	
def rfid_state(rq):
	if rq.method == "POST":
		Seesion = env["getModel"]("Seesion")
		User = env["getModel"]("User")
		Rfid = env["getModel"]("User")
		try: 
			session = Session.objects.get(session_hash=env["sessid"](rq))
			userr = session.user
		except Exception as e:
			return redirect("/%s/account.settings?error=%s" % (app_base, str(e)))
		
		rfid = Rfid.objects.get(user = userr)
		
		if rfid.active == True:
			rfid.active = False
		else:
			rfid.active = True
		rfid.save()
	return redirect("/%s/account.settings?msg=Password updated" % app_base)
		
		