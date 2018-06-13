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

    def def_talk(push):
        res = client.talk(push)
        
        json_dict = {"speech": output_text,
                     "displayText": output_text,
                     "source": "apiai-news"}
        
        return json_dict
    

def main():
    pass

if __name__ == '__main__':
    main()

