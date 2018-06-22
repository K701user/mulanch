# coding=utf-8
import pya3rt
import csv
import calendar
import datetime
import json
import random
import re

import requests

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn
)
from linebot.models import (
    PostbackAction, MessageAction, URIAction
)

from janome.tokenizer import Tokenizer


talk_apikey = "E1HZR7u2fuhdtBbrATJN5yBYK5atFTl9"
client = pya3rt.TalkClient(talk_apikey)

sample_members = {
                  "ななし":["かな", "性別", "年齢", "職業","特技","Rating","portforio url"],
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
        try:
            print(push)
            res = client.talk(push)
            print(res)
        except Exception as e:
            return {"error":e.message}
        
        json_dict = {"fulfillmentText": res["results"][0]["reply"],
                     "source": "reply"}
        
        return json_dict
   
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
            return self.post_carousel(member_list)
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
    def post_carousel(member_list):
        payload = {
            "messages":[
                {
                    "platform": "line",
                    "carouselBrowse":{
                    "items": [
                            {
                              "image": {"url":"http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800))},
                              "title": member_list[0][0] + "(" + member_list[0][1][0] + ")",
                              "description":  member_list[0][1][3] + ":" + member_list[0][1][4] + "(" + member_list[0][1][5] + ")",
                              "openUrlAction": 
                                  {
                                      "url": member_list[0][1][-1]
                                  }
                            },
                            {
                              "image": {"url":"http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800))},
                              "title": member_list[1][0] + "(" + member_list[1][1][0] + ")",
                              "description":  member_list[1][1][3] + ":" + member_list[1][1][4] + "(" + member_list[1][1][5] + ")",
                              "openUrlAction": 
                                  {
                                      "url": member_list[1][1][-1]
                                  }
                            },
                            {
                              "image": {"url":"http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800))},
                              "title": member_list[2][0] + "(" + member_list[2][1][0] + ")",
                              "description":  member_list[2][1][3] + ":" + member_list[2][1][4] + "(" + member_list[2][1][5] + ")",
                              "openUrlAction": 
                                  {
                                      "url": member_list[2][1][-1]
                                  }
                            }
                        ]
                    }
                  }
                ]
        }
        
        image_carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800)),
                        title= member_list[0][0] + "(" + member_list[0][1][0] + ")",
                        text= member_list[0][1][3] + ":" + member_list[0][1][4] + "(" + member_list[0][1][5] + ")",
                        actions=[
                            PostbackAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message1',
                                text='message text1'
                            ),
                            URIAction(
                                label='member_portfolio',
                                uri=member_list[0][1][-1]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800)),
                        title= member_list[1][0] + "(" + member_list[1][1][0] + ")",
                        text= member_list[1][1][3] + ":" + member_list[1][1][4] + "(" + member_list[1][1][5] + ")",
                        actions=[
                            PostbackAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageAction(
                                label='message2',
                                text='message text2'
                            ),
                            URIAction(
                                label='member_portfolio',
                                uri=member_list[1][1][-1]
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="http://pictogram2.com/p/p0{0:03d}/1.jpg".format(random.randint(100, 800)),
                        title= member_list[2][0] + "(" + member_list[2][1][0] + ")",
                        text= member_list[2][1][3] + ":" + member_list[2][1][4] + "(" + member_list[2][1][5] + ")",
                        actions=[
                            PostbackAction(
                                label='postback3',
                                text='postback text3',
                                data='action=buy&itemid=3'
                            ),
                            MessageAction(
                                label='message3',
                                text='message text3'
                            ),
                            URIAction(
                                label='member_portfolio',
                                uri=member_list[2][1][-1]
                            )
                        ]
                    )
                ]
            )
        )
  
        print(payload)
        return payload, image_carousel_template_message
    
    
def main():
    pass


if __name__ == '__main__':
    main()

