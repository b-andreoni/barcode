import cv2 as cv
import numpy as np
import pyzbar.pyzbar as pyzbar

def add_to_list_if_not_exists(mydata, data_list):
    if mydata not in data_list:
        data_list.append(mydata)
    return data_list

def adjust_brightness_contrast(frame, brightness=0, contrast=0):
    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    return frame

def detector(video_path):

    data_list = []  # Initialize an empty list to store unique mydata

    # Initialize the video capture
    video = cv.VideoCapture(video_path)

    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Check image quality (focus and lighting)
        #gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #if cv.Laplacian(gray_frame, cv.CV_64F).var() < 1000:
        #    print("Ignoring low-quality frame")
        #    continue 

        # Adjust brightness and contrast
        frame = adjust_brightness_contrast(frame, brightness=50, contrast=20)

        # Convert the frame to grayscale
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        thresh_frame = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

        # Find contours
        contours, _ = cv.findContours(thresh_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Find barcodes and Qr
        for contour in contours:
            approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)

            if len(approx) == 4:  # Check if the contour is approximately a rectangle
                # Convert the contour to a format compatible with pyzbar
                points = approx[:, 0, :]
                barcode_polygon = [tuple(point) for point in points]
                barcode_polygon = np.array(barcode_polygon, np.int32)

                # Find barcodes in the frame
                barcodes = pyzbar.decode(gray_frame, symbols=[pyzbar.ZBarSymbol.CODE128, pyzbar.ZBarSymbol.EAN13, pyzbar.ZBarSymbol.EAN8, pyzbar.ZBarSymbol.QRCODE])

                for barcode in barcodes:
                    mydata = barcode.data.decode('utf-8')
                    print(mydata)

                    # Add mydata to the list if it doesn't exist
                    data_list = add_to_list_if_not_exists(mydata, data_list)

                    # Draw a bounding box around the barcode
                    cv.polylines(frame, [barcode_polygon], True, (255, 0, 0), 5)

                    # Add text over the bounding box
                    x, y, w, h = cv.boundingRect(barcode_polygon)
                    cv.putText(frame, mydata, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

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
