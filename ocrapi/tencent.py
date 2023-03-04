import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from . import config
from .OCRBase import OCRBase
import os
import logging


class TencentOCR(OCRBase):
    def __init__(self, secrectId = config.SecrectId, secrectKey = config.SecretKey) -> None:
        
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(secrectId, secrectKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

    def request_base64(self, img):
        try:
            if isinstance(img, bytes):
                img = img.decode()

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralBasicOCRRequest()
            params = {
                "ImageBase64": img,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralBasicOCRResponse的实例，与请求对象对应
            resp = self.client.GeneralBasicOCR(req)

        except TencentCloudSDKException as err:
            logging.error(err)
        
        return resp
    
    def request_url(self, url):
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GeneralBasicOCRRequest()
            params = {
                "ImageUrl": url,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个GeneralBasicOCRResponse的实例，与请求对象对应
            resp = self.client.GeneralBasicOCR(req)
        
        except TencentCloudSDKException as err:
            logging.error(err)
        
        return resp

    def recongnize(self, img):
        if os.path.exists(img):
            resp = self.request_url(img)
        else:
            resp = self.request_base64(img)
        res = resp.TextDetections
        return " ".join(e.DetectedText for e in res)
