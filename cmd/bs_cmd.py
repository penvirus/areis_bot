# -*- coding: utf-8

from . import cmd, config
from mod_cmd import is_mod
import random

_bullshit = list()
_bullshit.append(u'在非洲，每六十秒，就有一分鐘過去')
_bullshit.append(u'凡是每天喝水的人，有高機率在100年內死去')
_bullshit.append(u'每呼吸60秒，就減少一分鐘的壽命')
_bullshit.append(u'當你吃下吃下廿碗白飯，換算竟相當於吃下了二十碗白飯的熱量')
_bullshit.append(u'誰能想的到，這名16歲少女，在四年前，只是一名12歲少女')
_bullshit.append(u'當你在睡覺休息時，美國人正勤奮的在工作')
_bullshit.append(u'當蝴蝶在南半球拍了兩下翅膀，牠就會稍微飛高一點點')
_bullshit.append(u'據統計，未婚生子的人數中有高機率為女性')
_bullshit.append(u'只要每天省下買一杯奶茶的錢，十天後就能買十杯奶茶')
_bullshit.append(u'當你的左臉被人打，那你的左臉就會痛')
_bullshit.append(u'今年中秋節剛好是滿月、今年七夕恰逢鬼月、今年母親節正好是星期日')
_bullshit.append(u'人被殺，就會死。')
_bullshit.append(u'台灣競爭力低落，在美國就連小學生都會說流利的英語')
def get_inline_bullshit():
    return random.choice(_bullshit)

def save_bullshit(sender, msg):
    bullshit = '%s (by %s)' % (msg, sender.name)

    config['bullshit'].append(bullshit)
    if len(config['bullshit']) > 1000:
        config['bullshit'] = config['bullshit'][1:]



@cmd('/bs')
def func_bs(sender, msg, receiver):
    if config['bullshit']:
        if is_mod(sender):
            for i in xrange(10):
                receiver.sendMessage(random.choice(config['bullshit']))
        else:
            receiver.sendMessage(random.choice(config['bullshit']))
    else:
        receiver.sendMessage(u'重播廢話失敗，沒有資料')
