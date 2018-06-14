# coding=utf-8
import pya3rt
import csv
import calendar
import datetime
import json
import random
import re

import requests

from janome.tokenizer import Tokenizer

talk_apikey = "E1HZR7u2fuhdtBbrATJN5yBYK5atFTl9"
client = pya3rt.TalkClient(talk_apikey)

class talker:
    def __init__(self, parent=None):
        pass

    @staticmethod
    def default_talk(push):
        try:
            print(push)
            res = client.talk(push)
            print(res)
        except Exception as e:
            return {"error":e.message}
        
        json_dict = {"speech": res["results"][0]["reply"],
                     "displayText": res["results"][0]["reply"],
                     "source": "reply"}
        
        return json_dict
    

def main():
    pass

if __name__ == '__main__':
    main()

