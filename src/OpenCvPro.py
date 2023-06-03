import cv2
import numpy as np
from pyzbar.pyzbar import decode

class OpenCvPro():
    def __init__(self):
        self.thickness = 1
        
    def barcode_read(self,frame,color):
        for barcode in decode(frame):
            myData:str = barcode.data.decode('utf-8')
            print(myData)
            print(color)
            
            x, y, w, h = barcode.rect
            qr_code_region = frame[y:y+h, x:x+w].copy()
            blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)
            blurred_frame[y:y+h, x:x+w] = qr_code_region
            
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, color, self.thickness *2) 
            pts2 = barcode.rect                                  #
            cv2.putText(blurred_frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, self.thickness*0.2, color, 2)
            #cv2.imshow('Blurred Frame', blurred_frame)
            frame[:]=blurred_frame[:]
    
    def camera_capture(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return self.video_capture
    
