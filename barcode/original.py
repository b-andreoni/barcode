# Install zbar and Pyzbar (pyzbar only if you are using Python version 3 or later)
# !pip install zbar
# !pip install pyzbar

import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pzb

def detector(video_path): 
    
    webcam = cv.VideoCapture(video_path)  # Initialize the video capture using the video file
    
    fps = webcam.get(cv.CAP_PROP_FPS)

    while True:
        ret, frame = webcam.read()
        
        
        if not ret:
            break

        if fps > 0:
            cv.waitKey(int(1000 / fps))

        for barcode in pzb.decode(frame):
            mydata = barcode.data.decode('utf-8')
            print(mydata)
            
            points = np.array([barcode.polygon], np.int32)
            points = points.reshape(-1, 1, 2)
            cv.polylines(frame, [points], True, (255, 0, 0), 5)
            
            points2 = barcode.rect
            pos = (points2[0], points2[1])
            x, y = pos
            text_size, _ = cv.getTextSize(mydata, cv.FONT_HERSHEY_SIMPLEX, 1, 0)
            text_w, text_h = text_size
            cv.rectangle(frame, pos, (x + text_w, y - text_h), (255, 0, 0), -1)
            cv.putText(frame, mydata, pos, cv.FONT_HERSHEY_SIMPLEX,
                      0.9, (255, 255, 255), 2)

        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('d'):
            webcam.release()
            cv.destroyAllWindows()
            break

if __name__ == '__main__':
    # Pass the video file path to the detector function
    video_path = "captura2.mp4"  # Replace with the actual video file path
    detector(video_path)
