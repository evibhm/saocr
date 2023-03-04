import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ocrapi.tencent import TencentOCR
from ocrapi.paddle import CPUPaddleOCR
from ocrapi.enhance import enhance
import base64
import numpy as np
import cv2

class Item(BaseModel):
    img: str
    enhance: bool = False

app = FastAPI()

router = APIRouter(prefix="/api")

paddleOCR = CPUPaddleOCR()
tencentOCR = TencentOCR()

@router.get("/paddle")
async def paddle():
    return PlainTextResponse("请使用Post请求")


@router.post("/paddle")
async def paddle(item: Item):
    if item.img:
        img = item.img
    else:
        return PlainTextResponse("图片不存在")
    try:
        img = img.split('base64,')[1]
    except:
        img = item.img
    if item.enhance:
        img = enhance(img)
    if img == "增强错误":
        img = item.img
    try:
        imgbytes = base64.b64decode(img)
    except:
        return PlainTextResponse("Base64解码失败")
    nparr = np.frombuffer(imgbytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = paddleOCR.recongnize(img)
    return PlainTextResponse(res)


@router.get("/tencent")
async def tencent():
    return PlainTextResponse("请使用Post请求")

@router.post("/tencent")
async def tencent(item: Item):
    if item.img:
        img = item.img
    else:
        return PlainTextResponse("图片不存在")
    try:
        img = img.split('base64,')[1]
    except:
        img = item.img
    if item.enhance:
        img = enhance(img)
    if img == "增强错误":
        img = item.img
    res = tencentOCR.recongnize(item.img)
    return PlainTextResponse(res)

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)