import httplib
from HTMLParser import HTMLParser
import requests
import json

from simgtd import settings


def send_due_notification(phone, template, thing, subject, date, url):
    conn = httplib.HTTPSConnection('leancloud.cn')
    conn.connect()

    header = {
        "X-AVOSCloud-Application-Id": settings.LeanCloudAppId,
        "X-AVOSCloud-Application-Key": settings.LeanCloudAppKey,
        "Content-Type": "application/json",
    }

    body_d = {
        "mobilePhoneNumber": phone,
        "template": template,
        "thing": thing,
        "subject": subject,
        "date": date,
        "url": url
    }

    body = json.dumps(body_d)
    conn.request('POST', '/1.1/requestSmsCode', body, header)
    conn.close()


def send_due_notification2(phone, template, thing, subject, date, url):
    api = 'https://leancloud.cn/1.1/requestSmsCode'

    headers = {
        "X-AVOSCloud-Application-Id": settings.LeanCloudAppId,
        "X-AVOSCloud-Application-Key": settings.LeanCloudAppKey,
        "Content-Type": "application/json",
    }

    h = HTMLParser()
    body_d = {
        "mobilePhoneNumber": phone,
        "template": template,
        "thing": thing,
        "subject": h.unescape(subject),
        "date": date,
        "url": url
    }

    return requests.post(api, data=json.dumps(body_d), headers=headers, verify=False)


if __name__ == '__main__':
    anders = '13456780123'
    #send_due_notification(anders, 'duedate', 'goal', 'subject', '11/06/2014', 'http://simplegtd.me/')
    resp = send_due_notification2(anders, 'duedate', 'goal', 'subject', '11/06/2014', 'http://simplegtd.me/')


