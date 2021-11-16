# encoding: utf-8
# @Author : GaoCG
# @File : run.py

import argparse
from Spyder.loopUtil.DateLoop import loop


def configSet():
    spyder_config = argparse.ArgumentParser()
    spyder_config.add_argument('--url', type=str, default="mmm", required=False)
    spyder_config.add_argument('--username', type=str, default="username", required=False)
    spyder_config.add_argument('--password', type=str, default="password", required=False)
    return spyder_config.parse_args()


def run():
    spyder_config = configSet()
    loop(spyder_config)
