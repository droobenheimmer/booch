# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 22:48:40 2017

@author: David Roberts
"""

import requests

client_key = "eOwPF6vr8WRIfL18Mz7hH9Pc0sgiX4BZGdGOjCPtgPl"

r = requests.post('https://maker.ifttt.com/trigger/kombucha_reading/with/key/eOwPF6vr8WRIfL18Mz7hH9Pc0sgiX4BZGdGOjCPtgPl', json={"value1": "asdfjkl"})

print(r.status_code)