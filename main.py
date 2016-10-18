# -*- coding: utf-8

from line_auth_token import LineClient as AuthClient
from line import LineClient
from cmd import cmds, save_conf, save_bullshit, is_mod, is_open_service
import traceback

token = AuthClient(id='YOUR_USERNAME', password='YOUR_PASSWORD', com_name='Areis Bot').authToken
c = LineClient(authToken=token, com_name='Areis Bot')

all_groups = list()
all_groups.append('DUMMY_GROUP_ID')
h_all_groups = frozenset(all_groups)



print 'Areis bot is ready'
while True:
    try:
        for op in c.longPoll(count=1):
            sender = op[0]
            receiver = op[1]
            message = op[2]

            if receiver.id not in h_all_groups:
                continue

            if message.text is None:
                # Stick
                continue

            try:
                message.text[0]
            except IndexError:
                # Stick
                continue

            if message.text[0] != '/':
                save_bullshit(sender, message.text)
            else:
                if not is_open_service() and not is_mod(sender):
                    continue
                cmd = message.text.split()[0].lower()
                try:
                    cmds[cmd](sender, message.text, receiver)
                except KeyError:
                    receiver.sendMessage(u'執行失敗，不存在的指令: %s' % cmd)
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
save_conf()
