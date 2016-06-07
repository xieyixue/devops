#!/usr/bin/env python
# coding=utf-8
__author__ = 'xieyixue'

from common.WXBizMsgCrypt import WXBizMsgCrypt
from devops.settings import (
    WXToken,
    WXCorpID,
    WXEncodingAESKey
)

class WxAPI(object):
    """
    处理微信消息加解密
    """

    def process_request(self, request):
        """
        入口： 解密
        :param request:
        :return:
        """

        sReqMsgSig = request.GET.get("msg_signature", None)
        sReqTimeStamp = request.GET.get("timestamp", None)
        sReqNonce = request.GET.get("nonce", None)

        if sReqMsgSig:
            wxcpt = WXBizMsgCrypt(WXToken, WXEncodingAESKey, WXCorpID)

            req_data = request.body
            ret, msg = wxcpt.DecryptMsg(req_data, sReqMsgSig, sReqTimeStamp, sReqNonce)

            if ret == 0:
                request.wx = msg