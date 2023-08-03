# Install zbar and Pyzbar (pyzbar only if you are using Python version 3 or later)
#!pip install zbar
#!pip install pyzbar

# Import libraries 
import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

def add_to_list_if_not_exists(mydata, data_list):
    if mydata not in data_list:
        data_list.append(mydata)
    return data_list

def detector(video_path):

    data_list = []  # Initialize an empty list to store unique mydata

    # Initialize the video capture
    video = cv.VideoCapture(video_path)

    while(True):
      
        # Capture the video frame by frame
        ret, frame = video.read()
        
        fps = video.get(cv.CAP_PROP_FPS)

        if not ret:
            break

        if fps > 0:
            cv.waitKey(int(100 / fps))

        # Find barcodes and Qr
        for barcode in pyzbar.decode(frame):
            
            # Convert the data from bytes to string
            mydata = barcode.data.decode('utf-8')
            print(mydata)
            
            # Add mydata to the list if it doesn't exist
            data_list = add_to_list_if_not_exists(mydata, data_list)
            
            # Add bounding box to qr codes and barcodes
            points = np.array([barcode.polygon], np.int32)
            points = points.reshape(-1, 1, 2)
            cv.polylines(frame, [points], True, (255, 0, 0), 5) # draw a polygon on an image
            
            # Add text over the bounding box
            points2 = barcode.rect
            cv.putText(frame, mydata, (points2[0], points2[1]), cv.FONT_HERSHEY_SIMPLEX,
                      0.9, (255, 0, 0), 2)
  
        # Display the resulting frame
        cv.imshow('frame', frame)
      
        # The 'q' button is set as the quitting button
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video and close window
    video.release()
    cv.destroyAllWindows()
    print(data_list)

# Main             
if __name__ == '__main__':
    # Pass the video file path to the detector function
    video_path = "slow.mp4"  # Replace with the actual video file path
    detector(video_path)
