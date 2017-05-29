import conf
from core.models import Log


def log(message):
	new_log = Log(message=message)
	new_log.save()
	if conf.verbose:
		print "[%s] [syzacz] %s" % (new_log.timestamp, message)
