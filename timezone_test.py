#!/usr/bin/python3

import time

def make_localtime(tstr):
    """Convert HH:MM in UTC to HH:MM in local timezone."""
    # hours west of UTC
    offset_h = time.timezone // 3600 # hours west of UTC
    # subtract offset, reduce mod24, cast to str
    local_h = str((int(tstr[:2]) - offset_h + 24) % 24)
    # get minutes
    local_m = tstr[3:]
    return "{}:{}".format(local_h, local_m)

t_old = "17:30"
t_new = make_localtime(t_old)

print("UTC time\t{}".format(t_old))
print("Local time\t{}".format(t_new))
