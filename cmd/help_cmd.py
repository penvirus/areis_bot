# -*- coding: utf-8

from . import cmd, config
from bs_cmd import get_inline_bullshit
from mod_cmd import is_mod
import operator

@cmd('/h')
def func_help(sender, msg, receiver):
    help_msg = list()

    help_msg.append(u'歡迎生活上有餘力的支持者贊助捐贈。')
    help_msg.append(u'  /text -- 列出所有文字指令')
    help_msg.append(u'  /img -- 列出所有圖片指令')
    help_msg.append(u'  /addt -- 新增文字指令')
    help_msg.append(u'  /addi -- 新增圖片指令')
    help_msg.append(u'  /del -- 刪除文字或圖片指令')
    help_msg.append(u'  /bs -- 隨機重播一句廢話')

    if is_mod(sender):
        help_msg.append(u'感謝您的贊助，您擁有額外的能力:')
        help_msg.append(u'  /del -- 刪除文字或圖片指令，即使是他人定義的')
        help_msg.append(u'  /bs -- 隨機重播「十」句廢話')
        help_msg.append(u'  /suspend -- 暫停服務非贊助會員')
        help_msg.append(u'  /resume -- 重新服務非贊助會員')

    receiver.sendMessage('\n'.join(help_msg))

@cmd('/text')
def func_text(sender, msg, receiver):
    help_msg = list()

    help_msg.append(get_inline_bullshit())
    help_msg.append('')
    help_msg.append(u'文字指令:')
    for k,v in sorted(config['text'].items(), key=operator.itemgetter(0)):
        help_msg.append('  /%s -- %s (by %s)' % (k, v['comment'], v['creater']))

    receiver.sendMessage('\n'.join(help_msg))

@cmd('/img')
def func_img(sender, msg, receiver):
    help_msg = list()

    help_msg.append(get_inline_bullshit())
    help_msg.append('')
    help_msg.append(u'圖片指令:')
    for k,v in sorted(config['img'].items(), key=operator.itemgetter(0)):
        help_msg.append('  /%s -- %s (by %s)' % (k, v['comment'], v['creater']))

    receiver.sendMessage('\n'.join(help_msg))
