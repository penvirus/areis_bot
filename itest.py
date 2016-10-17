# -*- coding: utf-8

from line_auth_token import LineClient as AuthClient
from line import LineClient
from cmd import cmds, save_conf, save_bullshit
import traceback

token = AuthClient(id='YOUR_USERNAME', password='YOUR_PASSWORD', com_name='Areis Bot').authToken
c = LineClient(authToken=token, com_name='Areis Bot')

# dummy sender
class Sender(object):
    def __init__(self):
        self.name = 'Tester'
        self.id = 'Tester'
sender = Sender()

# dummy receiver, a real LINE group but you should be the only memeber
receiver = c.getGroupById('DUMMY_GROUP_ID')


print 'Itest Areis bot is ready'
while True:
    try:
        msg = raw_input('in: ')
        receiver.sendMessage('%s' % msg)

        cmd = msg.split()[0].lower()
        try:
            cmds[cmd](sender, msg, receiver)
        except KeyError:
            receiver.sendMessage(u'不存在的指令: %s' % cmd)
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
#save_conf()
