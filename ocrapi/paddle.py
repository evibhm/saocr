from paddleocr import PaddleOCR
from .OCRBase import OCRBase

class CPUPaddleOCR(OCRBase):
    def __init__(self) -> None:
        super().__init__()
        # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
        # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)  # need to run only once to download and load model into memory
            
    def recongnize(self, img):
        result = self.ocr.ocr(img, cls=True)
        result = result[0]
        txts = [line[1][0] for line in result]
        return " ".join(txts)