from core.version import Version

version = Version([0, 0, 5, "testing"])
app_base = "syzacz/%s" % version.url()
verbose = True
plugin_blacklist = ["testplugin", "secondtestplugin"]
