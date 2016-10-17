# -*- coding: utf-8

from . import cmd, config

mods = frozenset(['DUMMY_MOD_ID'])

def is_mod(sender):
    return sender.id in mods

def is_open_service():
    return config['open_service']

def check_mod(sender, receiver):
    if not is_mod(sender):
        receiver.sendMessage(u'這是贊助者獨有功能')
        return False
    return True

@cmd('/suspend')
def func_suspend(sender, msg, receiver):
    if not check_mod(sender, receiver):
        return

    if not is_open_service():
        receiver.sendMessage(u'己經在贊助者模式')
    else:
        receiver.sendMessage(u'%s 切換至贊助者模式' % sender.name)
        config['open_service'] = False

@cmd('/resume')
def func_resume(sender, msg, receiver):
    if not check_mod(sender, receiver):
        return

    if is_open_service():
        receiver.sendMessage(u'己經在開放模式')
    else:
        receiver.sendMessage(u'%s 切換至開放模式' % sender.name)
        config['open_service'] = True
