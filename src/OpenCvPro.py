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
            pts2 = barcode.rect

            # Create a mask for the QR code region
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [pts], -1, 255, -1)

            # Apply Gaussian blur to the region outside the QR code
            blurred = cv2.GaussianBlur(frame, (51, 51), 0)
            blurred[mask.astype(bool)] = frame[mask.astype(bool)]

            # Draw the QR code bounding box and text on the blurred frame
            cv2.polylines(blurred, [pts], True, color, 5)
            cv2.putText(blurred, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Assign the blurred frame back to the original frame
            frame[:] = blurred[:]
    
    def camera_capture(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        return self.video_capture