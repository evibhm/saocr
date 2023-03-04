from abc import ABCMeta, abstractmethod

class OCRBase(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def recongnize(self, img):
        pass