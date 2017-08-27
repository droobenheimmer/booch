# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:16:04 2017

@author: David Roberts
"""

import argparse

parser = argparse.ArgumentParser(description='Retrieve arguments')
parser.add_argument('--batch', nargs='?', const=1, type=int)
args = parser.parse_args()

BATCH_ID = args.batch

print(BATCH_ID)