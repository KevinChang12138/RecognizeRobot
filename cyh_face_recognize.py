#! usr/bin/python #coding=utf-8
import http.client, urllib, base64, json
#import pandas as pd
import os

from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def localpic():
    src = input("输入本地图片路径（以/为分隔符）：")
    filename = src.split('/')
    filename = filename[len(filename) - 1]
    ftp = ftpconnect("118.89.157.146", "picture", "sanguo")
    uploadfile(ftp, filename, src)

    ftp.quit()
    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '7d0e0b3ead904df6ae853b1f8b057a24'

    uri_base = 'api.cognitive.azure.cn'

    # Request headers.
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

    # The URL of a JPEG image to analyze.
    body = "{'url':'http://118.89.157.146/" + filename + "'}"

    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = bytes.decode(data)
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        emotion = 'anger'
        evalue = 0.0
        emotion_list = {'anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'}
        for i in emotion_list:
            if (parsed[0]['faceAttributes']['emotion'][i] > evalue):
                emotion = i
                evalue = parsed[0]['faceAttributes']['emotion'][i]
        hair = 'brown'
        hvalue = 0.0
        hair_list = {'brown', 'black', 'red', 'gray', 'blond'}
        for i in [1, 5]:
            if (parsed[0]['faceAttributes']['hair']['hairColor'][i]['confidence'] > hvalue):
                hair = parsed[0]['faceAttributes']['hair']['hairColor'][i]['color']
                hvalue = parsed[0]['faceAttributes']['hair']['hairColor'][i]['confidence']

        print("图片中的信息为:")
        print("年龄:" + str(parsed[0]['faceAttributes']['age']))
        print("性别：" + str(parsed[0]['faceAttributes']['gender']))
        print("情感:" + str(emotion))
        print("发色：" + str(hair))
        print("清晰度：" + str(parsed[0]['faceAttributes']['blur']['blurLevel']))
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
        os.system("pause")

    except Exception as e:
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print("error")

def sitepic():
    subscription_key = '7d0e0b3ead904df6ae853b1f8b057a24'

    uri_base = 'api.cognitive.azure.cn'

    # Request headers.
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

    # The URL of a JPEG image to analyze.
    print("请输入网络图片url:")
    tmp = input()
    # body = "{'url':'https://wx2.sinaimg.cn/mw690/ba6a996fgy1fqa4qp5qsxj21401h9ncz.jpg'}"
    body = "{'url':'" + tmp + "'}"
    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        # sorted(parsed, key= lambda item: item[''])
        emotion = 'anger'
        evalue = 0.0
        emotion_list = {'anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'}
        for i in emotion_list:
            if (parsed[0]['faceAttributes']['emotion'][i] > evalue):
                emotion = i
                evalue = parsed[0]['faceAttributes']['emotion'][i]
        hair = 'brown'
        hvalue = 0.0
        hair_list = {'brown', 'black', 'red', 'gray', 'blond'}
        for i in [1, 5]:
            if (parsed[0]['faceAttributes']['hair']['hairColor'][i]['confidence'] > hvalue):
                hair = parsed[0]['faceAttributes']['hair']['hairColor'][i]['color']
                hvalue = parsed[0]['faceAttributes']['hair']['hairColor'][i]['confidence']

        print("图片中的信息为:")
        print("年龄:" + str(parsed[0]['faceAttributes']['age']))
        print("性别：" + str(parsed[0]['faceAttributes']['gender']))
        print("情感:" + str(emotion))
        print("发色：" + str(hair))
        print("清晰度：" + str(parsed[0]['faceAttributes']['blur']['blurLevel']))

        # data1 =json.dumps(parsed, sort_keys=True, indent=2)
        # print(data1)
        # print(data1[0].faceAttributes)
        # json = demjson.encode(data1)
        # print(json)
        conn.close()
        os.system("pause")

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
    choice=input("请选择传本地图片还是网络图片，输入1代表本地图片，输入2代表网络图片url：")
    if(choice=='1'):
        localpic()
    else:
        sitepic()
