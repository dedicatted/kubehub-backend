from os import system


def vbox_pkill():
    pkill_cmd = 'pkill VirtualBox'
    pkill = system(pkill_cmd)
    return pkill
