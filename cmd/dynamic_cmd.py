# -*- coding: utf-8

from . import cmd, config, cmds
from mod_cmd import is_mod
import os
import string
import requests
from functools import partial

valid_cmd_char = set(string.letters + string.digits)

def _send_text(sender, msg, receiver, entry):
    receiver.sendMessage(config['text'][entry]['src'])

def _send_img(sender, msg, receiver, filename):
    receiver.sendImage('img/%s' % filename)

def add_text_cmd(new_cmd):
    cmds['/' + new_cmd] = partial(_send_text, entry=new_cmd)

def add_img_cmd(route, filename):
    cmds['/' + route] = partial(_send_img, filename=filename)



@cmd('/addt')
def func_addt(sender, msg, receiver):
    args = msg.split()
    if len(args) < 3:
        receiver.sendMessage(u'用法: /addt <指令> <文字>...\n  指令: 英文數字組合')
        return

    new_cmd = args[1].lower()
    if len(set(new_cmd) - valid_cmd_char):
        receiver.sendMessage(u'新增失敗，指令含非法字元')
        return

    new_route = '/' + new_cmd
    if new_route in cmds:
        receiver.sendMessage(u'新增失敗，不允許重複定義指令')
        return

    text = (' '.join(args[2:]))
    if len(text) > 360:
        receiver.sendMessage(u'新增失敗，文字長度超過360位元組')
        return

    if len(text) > 16:
        comment = text[:16].decode('UTF-8', errors='ignore') + '...'
    else:
        comment = text.decode('UTF-8')
    text = text.decode('UTF-8')
    config['text'][new_cmd] = dict(creater=sender.name, creater_id=sender.id, src=text, comment=comment)
    add_text_cmd(new_cmd)

    receiver.sendMessage(u'%s 新增了以下指令: %s' % (sender.name, new_cmd))

@cmd('/addi')
def func_addi(sender, msg, receiver):
    args = msg.split()
    if len(args) < 3:
        receiver.sendMessage(u'用法: /addi <指令> <網址> <註解>...\n  指令: 英文數字組合\n  網址: 指向png或jpg檔，不可超過2MB\n  註解: 可有可無')
        return

    new_cmd = args[1].lower()
    if len(set(new_cmd) - valid_cmd_char):
        receiver.sendMessage(u'新增失敗，指令含非法字元')
        return

    new_route = '/' + new_cmd
    if new_route in cmds:
        receiver.sendMessage(u'新增失敗，不允許重複定義指令')
        return

    url = args[2]
    try:
        r = requests.head(url, verify=False)
    except:
        receiver.sendMessage(u'新增失敗，下載檔案不成功')
        return

    if not r.ok:
        receiver.sendMessage(u'新增失敗，下載檔案不成功')
        return

    try:
        if int(r.headers['Content-Length']) > 2097152:
            receiver.sendMessage(u'新增失敗，檔案超過2MB')
            return
    except KeyError:
        receiver.sendMessage(u'新增失敗，位址伺服器未給定Content-Length')
        return

    try:
        r = requests.get(url, verify=False)
    except:
        receiver.sendMessage(u'新增失敗，下載檔案不成功')
        return

    if not r.ok:
        receiver.sendMessage(u'新增失敗，下載檔案不成功')
        return

    try:
        content_type = r.headers['Content-Type']
    except KeyError:
        receiver.sendMessage(u'新增失敗，位址伺服器未給定Content-Type')
        return

    if content_type == 'image/png':
        filename = new_cmd + '.png'
    elif content_type == 'image/jpeg':
        filename = new_cmd + '.jpg'
    else:
        receiver.sendMessage(u'新增失敗，只接受image/png及image/jpeg兩種Content-Type')
        return

    with open('img/%s' % filename, 'w') as f:
        f.write(r.content)

    comment = (' '.join(args[3:])).decode('UTF-8')
    config['img'][new_cmd] = dict(src=filename, creater=sender.name, creater_id=sender.id, comment=comment)
    add_img_cmd(new_cmd, filename)

    receiver.sendMessage(u'%s 新增了以下指令: %s' % (sender.name, new_cmd))

@cmd('/del')
def func_del(sender, msg, receiver):
    args = msg.split()
    if len(args) < 2:
        receiver.sendMessage(u'用法: /del <指令>\n  只有指令擁有者有權限刪除該指令')
        return

    del_cmd = args[1].lower()

    if del_cmd in config['text']:
        target_type = 'text'
        target = config['text'][del_cmd]
    elif del_cmd in config['img']:
        target_type = 'img'
        target = config['img'][del_cmd]
    else:
        receiver.sendMessage(u'刪除失敗，該文字或圖片指令不存在')
        return

    if not is_mod(sender) and sender.id != target['creater_id']:
        receiver.sendMessage(u'刪除失敗，只有指令擁有者有權限刪除該指令')
        return

    if target_type == 'img':
        os.unlink('img/%s' % config['img'][del_cmd]['src'])

    del config[target_type][del_cmd]
    del cmds['/' + del_cmd]

    receiver.sendMessage(u'%s 刪除了以下指令: %s' % (sender.name, del_cmd))
