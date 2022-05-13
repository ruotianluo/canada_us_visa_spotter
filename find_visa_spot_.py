# Find spot.
# from bs4 import BeautifulSoup
import requests
import json
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "/tuixue.online-visa/api"))
import tuixue.ais_reg as ais_reg
import tuixue.ais_reg_orig as ais_reg_orig
import tuixue.ais_login as ais_login


login_status = False
session = None
schedule_id = None


def ais_register():
    country_code = 'en-ca'
    email = '<YOUR EMAIL>'
    pswd = '<YOUR PASSWORD>'
    node = ''
    global session
    global schedule_id
    result = session = schedule_id = None
    try:
        result, session, schedule_id = ais_reg_orig.register(country_code, email, pswd, node)
    except Exception as e:
        print(e)
    return result, session, schedule_id


def ais_refresh():
    return ais_login.refresh('en-ca', schedule_id, session)


def is_early(slots):
    if type(slots[0]) == list:
        # rt's account, at pay page.
        for slot in slots:
            if slot[1][0] == 2022 and slot[1][1] <= 8:
                return True
        return False
    else:
        # # jin's account, at schedule page.
        # for slot in slots:
        #     # convert date to datetime
        #     dt = datetime.datetime.strptime(slot['date'], '%Y-%m-%d')
        #     if dt.year == 2022:
        #         return True
        return False


def find_spot():
    global login_status
    if login_status == False:
        result, _, __ = ais_register()
    # result = ais_refresh()
    if result:
        return str(result), is_early(result)
    else:
        return result, False


from typing import List
import os
import datetime
import time
import traceback
import functools
import json
import socket
import requests

DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z"
webhook_url = "https://hooks.slack.com/services/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"

def slack_sender(webhook_url: str, channel: str, message: str, content: str, user_mentions: List[str] = []):
    """
    Slack sender wrapper: execute func, send a Slack notification with the end status
    (sucessfully finished or crashed) at the end. Also send a Slack notification before
    executing func.
    `webhook_url`: str
        The webhook URL to access your slack room.
        Visit https://api.slack.com/incoming-webhooks#create_a_webhook for more details.
    `channel`: str
        The slack room to log.
    `user_mentions`: List[str] (default=[])
        Optional users ids to notify.
        Visit https://api.slack.com/methods/users.identity for more details.
    """

    dump = {
        "username": "DiskAlarm",
        "channel": channel,
        "icon_emoji": ":clapper:",
    }

    start_time = datetime.datetime.now()

    contents = [f'{content}. %{start_time.strftime(DATE_FORMAT)}']
    contents.append(message)
    contents.append(' '.join(user_mentions))
    dump['text'] = '\n'.join(contents)
    dump['icon_emoji'] = ':clapper:'
    requests.post(webhook_url, json.dumps(dump))


def call_sender():
    from twilio.rest import Client
    account_sid = '<YOUR ACCOUNT SID>'
    auth_token = '<YOUR AUTH TOKEN>'
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                            twiml='<Response><Say>There is a spot!!!!!</Say></Response>',
                            to='<YOUR NUMBER>',
                            from_='<YOUR TWILIO NUMBER>'
    )


import random
while True:
    slack_content, spot_flag = find_spot()
    print(slack_content)
    if spot_flag:
        slack_sender(webhook_url, 'knockknock', '', slack_content, user_mentions=['<@U7M4XNTLL>'])
        call_sender()
    t = random.randint(15 * 60, 25 * 60)
    print(f'Sleep {t} seconds.')
    time.sleep(t)

