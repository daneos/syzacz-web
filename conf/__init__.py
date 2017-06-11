from core.version import Version

version = Version([0, 0, 4, "testing"])
app_base = "syzacz/%s" % version.url()
verbose = True
