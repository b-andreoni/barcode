import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

def add_to_list_if_not_exists(mydata, data_list):
    if mydata not in data_list:
        data_list.append(mydata)
    return data_list

def adjust_brightness_contrast(frame, brightness=0, contrast=0):
    # Adjust brightness and contrast using numpy operations
    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    return frame

def detector(video_path):
    data_list = []  # Initialize an empty list to store unique mydata

    # Initialize the video capture
    video = cv.VideoCapture(video_path)

    # Get the video properties
    fps = video.get(cv.CAP_PROP_FPS)
    total_frames = int(video.get(cv.CAP_PROP_FRAME_COUNT))

    # Set brightness and contrast once
    ret, frame = video.read()
    frame = adjust_brightness_contrast(frame, brightness=50, contrast=20)

    # Define the region of interest (ROI) where barcodes are likely to be present
    roi_height = int(frame.shape[0] * 0.6)
    roi = frame[roi_height:, :]

    # Skipping frames for performance improvement
    frame_skip = max(1, int(fps / 10))  # Skip 1/10th of a second frames
    current_frame = 0

    while(current_frame < total_frames):
        # Set the video to the current frame position
        video.set(cv.CAP_PROP_POS_FRAMES, current_frame)

        # Capture the video frame by frame
        ret, frame = video.read()
        if not ret:
            break

        # Skip frames for faster processing
        current_frame += frame_skip

        # Skip processing duplicate frames
        if current_frame % frame_skip != 0:
            continue

        # Resize frame to a smaller resolution for faster processing
        frame = cv.resize(frame, None, fx=0.5, fy=0.5)

        # Convert the frame to grayscale and extract the ROI
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        roi_gray = gray[roi_height:, :]

        # Find barcodes and QR codes
        for barcode in pyzbar.decode(roi_gray):
            # Convert the data from bytes to string
            mydata = barcode.data.decode('utf-8')
            print(mydata)

            # Add mydata to the list if it doesn't exist
            data_list = add_to_list_if_not_exists(mydata, data_list)

            # Add bounding box to QR codes and barcodes
            points = np.array([barcode.polygon], np.int32)
            points = points.reshape(-1, 1, 2)
            cv.polylines(frame, [points], True, (255, 0, 0), 5)  # draw a polygon on an image

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
    video_path = "captura2.mp4"  # Replace with the actual video file path
    detector(video_path)
