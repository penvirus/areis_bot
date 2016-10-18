# -*- coding: utf-8

from functools import wraps
import json
import random
import os
from glob import glob

CONFIG_PATH = 'config.json'

config = dict()

with open(CONFIG_PATH) as f:
    config = json.load(f)

def save_conf():
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ':'))



cmds = dict()

def cmd(route):
    def wrapped_cmd(func):
        cmds[route] = func
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped_func
    return wrapped_cmd

import help_cmd
from dynamic_cmd import add_text_cmd, add_img_cmd
from bs_cmd import save_bullshit
from mod_cmd import is_mod, is_open_service

for k, v in config['text'].items():
    add_text_cmd(k)

for k, v in config['img'].items():
    add_img_cmd(k, v['src'])
