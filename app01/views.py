# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import xml.etree.cElementTree as ET


from common.WXBizMsgCrypt import WXBizMsgCrypt
from wechat.official import (
    WxApplication,
    WxTextResponse,
    WxMusic,
    WxMusicResponse

)
# Create your views here.
sToken = "zViwQDUt6gPXkBGhwoRrLAtcUPqsr"
sEncodingAESKey = "2NABdq9wq63m4HNkd2KAsAOhOZjNcnhBr2i7XoHExkb"
sCorpID = "wx2eb99b2a4e38b99a"

class WeChatCall(APIView):

    def get(self, request):
        print request.DATA
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        sVerifyMsgSig = request.GET.get("msg_signature", None)
        sVerifyTimeStamp = request.GET.get("timestamp", None)
        sVerifyNonce = request.GET.get("nonce", None)
        sVerifyEchoStr = request.GET.get("echostr", None)

        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if (ret != 0):
            return Response(HTTP_400_BAD_REQUEST)

        return HttpResponse(sEchoStr)

    def post(self, request):

        # # sReqMsgSig = HttpUtils.ParseUrl("msg_signature")
        # sReqMsgSig = request.GET.get("msg_signature", None)
        sReqTimeStamp = request.GET.get("timestamp", None)
        sReqNonce = request.GET.get("nonce", None)
        wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
        #
        # sReqData = request.body
        # ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        # if (ret != 0):
        #     print "ERR: DecryptMsg ret: " + ret
        sMsg = request.wx

        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text
        print content
        sRespData = "<xml><ToUserName><![CDATA[mycreate]]></ToUserName><FromUserName><![CDATA[wx5823bf96d3bd56c7]]></FromUserName><CreateTime>1348831860</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{0}]]></Content><MsgId>1234567890123456</MsgId><AgentID>128</AgentID></xml>"
        sRespData = sRespData.format(content)
        ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)

        return HttpResponse(sEncryptMsg)


class Index(APIView):
    def get(self, request):
        return HttpResponse("ok")