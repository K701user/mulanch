# coding=utf-8
import pya3rt
import csv
import calendar
import datetime
import json
import random
import re

import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    MessageAction, URIAction, PostbackAction, CarouselTemplate, CarouselColumn
)

from janome.tokenizer import Tokenizer


talk_apikey = "DZZyF7nPhIQoS87LCI7vuIqfdeSElSB8"
client = pya3rt.TalkClient(talk_apikey)

sample_members = {
                  "揚出 剛史":["あげいでたけし", "male", "47", "医師", "対話による体調診断をおこないます。", "15", "https://www.google.com/"],
                  "川内谷 茜音":["かわうちやあかね", "female", "51", "主婦", "料理をしにいきます。", "3", "https://www.yahoo.co.jp/"],
                  "谷合 沙樹":["たにあいさき", "unknown", "private", "PM", "PG講座を行います。", "5", "https://www.msn.com/ja-jp"],
                  "旭爪 昌典":["ひのつめまさのり", "male", "60", "リタイア", "おはなし相手になります。", "1", "https://www.bing.com/"],
                  "乙幡 涼香":["おとはたすずか", "female", "41", "シェフ", "料理教室の講師を請け負います。", "33", "https://www.yahoo.co.jp/"]
                 }

class talker:
    def __init__(self, parent=None):
        pass

    @staticmethod
    def default_talk(push):
        response = {}
        
        try:
            print(push)
            res = client.talk(push)
            print(res)
            response["fulfillmentText"] = [
                    res["results"][0]["reply"] 
            ]
            response["payload"] = {
                "google": 
                {
                    "expectUserResponse": True,
                    "richResponse":
                    {
                        "items": 
                        [{
                            "simpleResponse": {
                                "textToSpeech": res["results"][0]["reply"] ,
                                "displayText": res["results"][0]["reply"]
                            }
                        }]
                    }
                }
            }

            
        except Exception as e:
            return {"error":e.message}

        print("Response:")
        print(response)

        #         json_dict = {"fulfillmentText": res["results"][0]["reply"],
        #                      "source": "reply"}

        return response
   
    def listup_member(self, push):
        try:
            print(push)
            keys = self.morphological_analysis(push)
            
            # member_list = pickup_members(keys)
            '''
            現在サンプルなのでリストはランダムに三人出しておく
            '''
            member_list = []
            for i in range(3):
                name, profile = random.choice(list(sample_members.items()))
                member_list.append([name, profile])    
            
            print(member_list)
            return self.listup_member_post_carousel(member_list)
        except Exception as e:
            print(e.args)
    
    @staticmethod
    def morphological_analysis(text):
        txt = text
        t = Tokenizer()
        word_dic = {}
        lines = txt.split("\r\n")
        for line in lines:
            blog_txt = t.tokenize(line)
            for w in blog_txt:
                word = w.base_form
                ps = w.part_of_speech
                if ps.find('名詞') < 0 and ps.find('形容詞') < 0:
                    continue
                if word not in word_dic:
                    word_dic[word] = 0
                word_dic[word] += 1

        keys = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)
        keyword = []
        for word, cnt in keys:
            print("{0} ".format(word))
            keyword.append(word)

        return keyword
        
    @staticmethod
    def listup_member_post_carousel(member_list):      
        image_carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://pictogram-illustration.com/material/7{0:02d}-pictogram-illustration.jpg".format(random.randint(1, 80)),
                        title= member[0] + "(" + member[1][0] + ")",
                        text= member[1][3] + ":" + member[1][4] + "(" + member[1][5] + ")",
                        actions=[
                            MessageAction(
                                label='この人に決める',
                                text=member[0]+'さんにアポイントをとってください。'
                            ),
                            URIAction(
                                label='member_portfolio',
                                uri=member[1][-1]
                            )
                        ]
                    )
                    for member in member_list
#                     CarouselColumn(
# #                        thumbnail_image_url="http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800)),
#                         title= member_list[1][0] + "(" + member_list[1][1][0] + ")",
#                         text= member_list[1][1][3] + ":" + member_list[1][1][4] + "(" + member_list[1][1][5] + ")",
#                         actions=[     
#                             MessageAction(
#                                 label='Translate Rice',
#                                 text='米'
#                             ),
#                             URIAction(
#                                 label='member_portfolio',
#                                 uri=member_list[1][1][-1]
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
# #                        thumbnail_image_url="http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800)),
#                         title= member_list[2][0] + "(" + member_list[2][1][0] + ")",
#                         text= member_list[2][1][3] + ":" + member_list[2][1][4] + "(" + member_list[2][1][5] + ")",
#                         actions=[
#                             MessageAction(
#                                 label='この人に決める',
#                                 text='３さんにアポイントをとってください。'
#                             ),
#                             URIAction(
#                                 label='member_portfolio',
#                                 uri=member_list[2][1][-1]
#                             )
#                         ]
#                     )
                ]
            )
        )
  
        print(image_carousel_template_message)
    
        return image_carousel_template_message
    
    
def main():
    pass


if __name__ == '__main__':
    main()

