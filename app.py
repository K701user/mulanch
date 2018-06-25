# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    URIAction, PostbackAction, MessageAction,
    CarouselTemplate, CarouselColumn
)

import talk_style

import json
import os
from flask import abort

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
line_bot_api = LineBotApi('F8Fkj5KU0iLcQC+QIc18RBgozcFV00veN0qf3aJfMhv15W+IotzpKBuOBBz9ulLvruwjgCHdw4mCNqwchuH3O7z4xkwLbyPGnloKOEcZ2UtCI9m2lg66k1LKCaAbEWg0LK2FBeaI+Q/v2lLxhInN9AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1d81556ec390b8eeb4da45ac8dae8d11')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print(r)
    return r


@app.route('/load-sql', methods=['GET'])
def load_sql():
    req = request.args.get('query')
    querylist = req.split('_')
    res = loadsqlRequest(querylist)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r, 200


def loadsqlRequest(req):
    reqtype = None
    q1 = None
    q2 = None
    date = None
    
    try:
        reqtype = req[0]
    except:
        pass
    try:
        q1 = req[1]
    except:
        pass
    try:
        q2 = req[2]
    except:
        pass
    try:
        date = req[3]
    except:
        pass
    try:
        if date is None:
            date = q2
            if date is None:
                date = datetime.date.today().strftime('%Y%m%d') 
    except:
        pass
    try:
        if type(date) is list:            
            date = date[0].replace('-', '')
        else:
            date = date.replace('-', '')
    except:
        print("Line send miss")
    
    try:
        if reqtype == "p":
            res = SL.execute_sql(q1, "bplayerrecord", "name", ["name", "record"], day=date)
        elif reqtype == "n":
            res = SL.execute_sql(q1, "newsrecord", "title", ["title", "row2_text"], day=date)
        elif reqtype == "s":
            res = SL.execute_sql2([q1, q2],"scorerecord", ["team1", "team2"], ["team1", "team2", "score"], day=date)
        else:
            return {}
    except:
        return {}
        
    return res


def processRequest(req):
    try:
        print(req)
        actiontype = req.get("queryResult").get("action")
        parameters = req.get("queryResult").get("parameters")
        q_text = req.get("queryResult").get("queryText")
        print(q_text)
    except:
        return {}
    
    talker = talk_style.talker()
    
    if "Matching_requeststart" in actiontype or "matchingrequeststart-followup" in req.get('outputContexts').get('name'):
        print("Matching_requeststart")
        res, postres = talker.listup_member(q_text)
        try:
            rtoken = req.get('originalDetectIntentRequest').get('payload').get('data').get('replyToken')
            print(rtoken)
            line_bot_api.reply_message(rtoken, postres)
        except Exception as e:
            print("line send error : " + e.args)
    else:
        print("Other")
        res = talker.default_talk(q_text)

    return res


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
