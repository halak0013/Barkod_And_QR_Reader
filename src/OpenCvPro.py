import cv2
import numpy as np
from pyzbar.pyzbar import decode

class OpenCvPro():
    def __init__(self):
        pass
    def barcode_read(self,frame,color):
        for barcode in decode(frame):
            myData:str = barcode.data.decode('utf-8')
            print(myData)
            print(color)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, color, 5)
            pts2 = barcode.rect
            cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    def camera_capture(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        return self.video_capture