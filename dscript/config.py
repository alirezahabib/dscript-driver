# Don't modify these values here (unless you want to change the defaults)
# modify them in your script (after the import)
pulse_duration = 0.050  # in seconds
slowdown = 0.010  # in seconds
settle_down = 0.500  # in seconds
ip_address = '169.254.100.1'
port = 80
connection_timeout = 4.0  # in seconds


def toggle_url(relay):
    return 'http://' + ip_address + '/dscript.cgi?V20552=' + str(relay)
